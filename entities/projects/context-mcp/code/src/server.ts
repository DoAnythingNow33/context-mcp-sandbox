// One MCP server per request (stateless): built for a single member of a single vault, so nothing
// about one caller can leak into another's request.

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { WebStandardStreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/webStandardStreamableHttp.js";
import { GetPromptRequestSchema, ListPromptsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";
import type { Member } from "./access";
import { VaultService, type Audit, type Backend, type Tenant } from "./vault";

const text = (t: string) => ({ content: [{ type: "text" as const, text: t }] });

export function buildServer(tenant: Tenant, member: Member, backend: Backend, audit: Audit): McpServer {
  const vault = new VaultService(tenant, member, backend, audit);
  const mcp = new McpServer(
    { name: `context-${tenant.id}`, version: "2.0.0" },
    {
      instructions:
        `This server is the '${tenant.name}' context vault: the shared source of truth as markdown files. ` +
        "Call get_map first: it returns the vault's map and routing rules, which say which files to read " +
        "for which task. Then use search / list_files / read_file. Context is additive: never rewrite " +
        "existing facts. Use append_to_file or create_file if your access allows it; otherwise use " +
        "raise_flag to propose a change for a human to confirm.",
    },
  );
  const readOnly = { readOnlyHint: true, openWorldHint: false };
  const additive = { readOnlyHint: false, destructiveHint: false, openWorldHint: false };

  mcp.registerTool(
    "get_map",
    {
      description:
        "Start here. Returns the vault's map (routing rules: what to read for which task), orientation files (compressed state of everything), and what you are allowed to do.",
      annotations: readOnly,
    },
    async () => text(await vault.getMap()),
  );
  mcp.registerTool(
    "list_files",
    {
      description: "List the files you can read, optionally under a folder (e.g. 'Growify/people').",
      inputSchema: { folder: z.string().default("") },
      annotations: readOnly,
    },
    async ({ folder }) => text(await vault.listFiles(folder)),
  );
  mcp.registerTool(
    "read_file",
    {
      description: "Read a vault file by its path relative to the vault root. Long files are paged: pass start_line to continue.",
      inputSchema: { path: z.string(), start_line: z.number().int().min(1).default(1), max_lines: z.number().int().min(1).max(2000).default(400) },
      annotations: readOnly,
    },
    async ({ path, start_line, max_lines }) => text(await vault.readFile(path, start_line, max_lines)),
  );
  mcp.registerTool(
    "search",
    {
      description: "Search file names and contents (case-insensitive; every word must appear in the file). Returns matching files with the lines that matched.",
      inputSchema: { query: z.string(), folder: z.string().default(""), max_results: z.number().int().min(1).max(50).default(15) },
      annotations: readOnly,
    },
    async ({ query, folder, max_results }) => text(await vault.search(query, folder, max_results)),
  );
  mcp.registerTool(
    "append_to_file",
    {
      description:
        "Add new context to the end of an existing file (additive; never rewrites what is there). `reason` is a short note of where this came from, e.g. 'call with Disha 1 Oct'.",
      inputSchema: { path: z.string(), content: z.string(), reason: z.string() },
      annotations: additive,
    },
    async ({ path, content, reason }) => text(await vault.appendToFile(path, content, reason)),
  );
  mcp.registerTool(
    "create_file",
    {
      description: "Create a new markdown file (fails if it already exists: append to it instead). Follow the vault's naming conventions from get_map.",
      inputSchema: { path: z.string(), content: z.string(), reason: z.string() },
      annotations: additive,
    },
    async ({ path, content, reason }) => text(await vault.createFile(path, content, reason)),
  );
  mcp.registerTool(
    "raise_flag",
    {
      description:
        "Propose a change for a human to confirm, instead of editing the source of truth. Use for: a fact that changes an existing entity, a contradiction, a new unverified client/tool/process, or a possible duplicate.",
      inputSchema: { entity: z.string(), change: z.string(), kind: z.enum(["update", "conflict", "new", "duplicate"]).default("update") },
      annotations: additive,
    },
    async ({ entity, change, kind }) => text(await vault.raiseFlag(entity, change, kind)),
  );

  // Skills come from the repo, so prompts are listed on demand rather than registered up front.
  mcp.server.registerCapabilities({ prompts: {} });
  mcp.server.setRequestHandler(ListPromptsRequestSchema, async () => ({
    prompts: (await vault.prompts()).map((p) => ({
      name: p.name,
      description: p.description,
      arguments: [{ name: "input", description: "Notes, transcript or request to run the workflow on", required: false }],
    })),
  }));
  mcp.server.setRequestHandler(GetPromptRequestSchema, async (req) => ({
    messages: [{ role: "user", content: { type: "text", text: await vault.prompt(req.params.name, req.params.arguments?.input ?? "") } }],
  }));

  return mcp;
}

export async function handleMcp(request: Request, tenant: Tenant, member: Member, backend: Backend, audit: Audit): Promise<Response> {
  if (request.method !== "POST") return new Response("Method not allowed", { status: 405, headers: { allow: "POST" } });
  const mcp = buildServer(tenant, member, backend, audit);
  const transport = new WebStandardStreamableHTTPServerTransport({ sessionIdGenerator: undefined, enableJsonResponse: true });
  await mcp.connect(transport);
  try {
    return await transport.handleRequest(request);
  } finally {
    await mcp.close();
  }
}
