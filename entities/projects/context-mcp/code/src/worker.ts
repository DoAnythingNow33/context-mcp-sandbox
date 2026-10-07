// Worker entry point. The vault is chosen by hostname (one entry point per vault), the member by
// their sign-in. Phase 3 signs in with a dev-only stub; Phase 4 swaps in OAuth + Google.

import type { Member } from "./access";
import { GitHubVault } from "./github";
import { handleMcp } from "./server";
import type { Audit, Backend, Tenant } from "./vault";

export interface Deps {
  tenantForHost(hostname: string): Tenant | undefined;
  /** The signed-in email for this request on this tenant, or undefined. */
  authenticate(request: Request, tenant: Tenant): Promise<string | undefined>;
  backendFor(tenant: Tenant): Backend;
  audit: Audit;
}

const unauthorized = () =>
  new Response(JSON.stringify({ error: "invalid_token", error_description: "Sign in to this vault first" }), {
    status: 401,
    headers: { "content-type": "application/json", "www-authenticate": 'Bearer realm="context-mcp"' },
  });

export function createApp(deps: Deps) {
  return async (request: Request): Promise<Response> => {
    const url = new URL(request.url);
    if (url.pathname === "/health") return new Response("ok");
    const tenant = deps.tenantForHost(url.hostname);
    if (!tenant) return new Response("Not found", { status: 404 });
    if (url.pathname !== "/mcp") return new Response("Not found", { status: 404 });
    const email = (await deps.authenticate(request, tenant))?.toLowerCase();
    const member: Member | undefined = email ? tenant.members.find((m) => m.email.toLowerCase() === email) : undefined;
    // Same answer for "no login" and "login that isn't a member here": don't confirm who belongs.
    if (!member) return unauthorized();
    return handleMcp(request, tenant, member, deps.backendFor(tenant), deps.audit);
  };
}

interface Env {
  /** JSON array of Tenant. Phase 4 moves this to a per-vault EU store. */
  TENANTS: string;
  /** PAT for Phase 3 only; Phase 4 uses a GitHub App installation token per tenant. */
  GITHUB_TOKEN: string;
  /** "1" enables `Authorization: Bearer dev:<email>`. Never set on a deployed Worker. */
  DEV_AUTH?: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const tenants: Tenant[] = JSON.parse(env.TENANTS);
    return createApp({
      tenantForHost: (host) => tenants.find((t) => t.hostname === host),
      authenticate: async (req) => {
        if (env.DEV_AUTH !== "1") return undefined;
        const auth = req.headers.get("authorization") ?? "";
        return auth.startsWith("Bearer dev:") ? auth.slice("Bearer dev:".length) : undefined;
      },
      backendFor: (t) => new GitHubVault({ ...t.repo, token: async () => env.GITHUB_TOKEN }),
      audit: (e) => console.log(JSON.stringify({ audit: e })),
    })(request);
  },
};
