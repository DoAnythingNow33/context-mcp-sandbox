import { describe, expect, it } from "vitest";
import { AccessError, canRead, canWrite, normalizePath, requireLevel, visibleFiles, type Member } from "../src/access";

const employee: Member = {
  email: "team@growify.example", name: "Growify team", write: "flag",
  read: ["Growify/**"], writePaths: ["Growify/**"],
  deny: ["Growify/people/_team-restructure.md", "Growify/_flags*", "Growify/_archive/**", "Growify/_status/**"],
};
const founder: Member = { email: "r@x", name: "Rishab", read: ["**"], deny: ["founders/Disha/self/**"], write: "create", writePaths: ["**"] };

describe("access", () => {
  it("employee sees business room only", () => {
    expect(canRead(employee, "Growify/CLAUDE.md")).toBe(true);
    expect(canRead(employee, "founders/Rishab/self/me.md")).toBe(false);
  });
  it("deny wins, including nested and flag queue", () => {
    expect(canRead(employee, "Growify/people/_team-restructure.md")).toBe(false);
    expect(canRead(employee, "Growify/_flags.md")).toBe(false);
    expect(canRead(employee, "Growify/_archive/old/a.md")).toBe(false);
  });
  it("founder sees all but the other founder's self/", () => {
    expect(canRead(founder, "Growify/people/_team-restructure.md")).toBe(true);
    expect(canRead(founder, "founders/Disha/self/x.md")).toBe(false);
  });
  it("dot paths and secrets are always hidden", () => {
    for (const p of [".git/config", "a/.obsidian/x.md", "a/.env", "a/secrets.md", "a/api.key", "a/credentials.json"])
      expect(canRead(founder, p)).toBe(false);
  });
  it("blocks path traversal", () => {
    expect(() => normalizePath("../../etc/passwd")).toThrow(AccessError);
    expect(() => normalizePath("a/../../b")).toThrow(AccessError);
    expect(normalizePath("/a//b/./c/../d.md")).toBe("a/b/d.md");
  });
  it("write levels", () => {
    expect(() => requireLevel(employee, "flag")).not.toThrow();
    expect(() => requireLevel(employee, "append")).toThrow(AccessError);
    expect(() => requireLevel(founder, "create")).not.toThrow();
    expect(canWrite(employee, "Growify/a.md")).toBe(true);
    expect(canWrite(employee, "other/a.md")).toBe(false);
  });
  it("visibleFiles filters and scopes", () => {
    const all = ["Growify/a.md", "Growify/_flags.md", "founders/x.md", "Growify/sub/b.md"];
    expect(visibleFiles(employee, all)).toEqual(["Growify/a.md", "Growify/sub/b.md"]);
    expect(visibleFiles(employee, all, "Growify/sub")).toEqual(["Growify/sub/b.md"]);
  });
});
