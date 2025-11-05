# Claude Skills

This directory contains custom skills for Claude Code. Skills are specialized capabilities that Claude can invoke autonomously when appropriate.

## How Skills Work

- Skills are stored in `.claude/skills/` (project-level) or `~/.claude/skills/` (personal)
- Each skill is a markdown file named `SKILL.md` in its own directory
- Claude automatically detects when to use skills based on context
- Skills can be invoked with the `/skill-name` command

## Skill Structure

Each skill directory should contain a `SKILL.md` file with:

1. **Name** - The skill name (directory name)
2. **Description** - When Claude should use this skill
3. **Instructions** - Detailed steps for Claude to follow

## Common Skill Examples

You can create skills for tasks like:

- PDF processing and analysis
- Excel/CSV data manipulation
- Code review workflows
- Commit message generation
- Documentation generation
- API testing

## Creating a New Skill

1. Create a new directory: `.claude/skills/my-skill/`
2. Add a `SKILL.md` file with the skill definition
3. Claude will automatically detect and use it when relevant

## Documentation

For more information, see: https://docs.claude.com/en/docs/claude-code/skills.md
