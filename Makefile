# The Agentic Security Auditor
# Python 3.9+, standard library only. No install step, no dependencies, no network.

.PHONY: verify register cite help

help:
	@echo "make verify              prove the standard is intact and every citation is honest"
	@echo "make verify FILE=x.md   check an audit you wrote against the same rules"
	@echo "                        add ARTIFACT=agent.md to check its claims about the agent"
	@echo "make register           regenerate provisions.md from the reference (deliberate act)"
	@echo
	@echo "  bash scripts/cite.sh ASI04-PIN           read one provision"
	@echo "  bash scripts/cite.sh --list              every provision id"
	@echo "  bash scripts/cite.sh --from examples.md  every citation in a document"

# Offline by design. An auditor you can only check when a server is reachable is
# a worse auditor, so nothing here touches the network.
# Pass FILE=path to check an audit you wrote instead of the repository itself.
verify:
	@python3 scripts/verify.py $(FILE) $(if $(ARTIFACT),--artifact $(ARTIFACT))

# Rebuilds the register from reference/. Only run this when the standard itself
# has been deliberately replaced: it is what makes a drifted citation visible,
# so regenerating it to silence a failure defeats the check.
register:
	@python3 scripts/build_register.py
	@echo
	@echo "Register rebuilt. Read 'git diff provisions.md' before committing:"
	@echo "a changed line means a citation somewhere now points at different words."
