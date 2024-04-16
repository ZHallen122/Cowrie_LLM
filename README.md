# Cowrie_LLM
This is the project based on Cowrie: https://github.com/cowrie/cowrie

# Setting up

## Software required to run locally same as cowrie:
    Python 3.8+
    python-virtualenv

    cd cowrie
    pip install -r requirements.txt

    Prepare gpt api at openai
    create a .env file in /LLM/GPT_3.5
    OPENAI_API_KEY=YOUR_API_KEY

Then Follow the oringinal Cowrie documentation After step1
https://cowrie.readthedocs.io/en/latest/INSTALL.html

# Folder structure
/logging    The analysis script folder
/cowrie    The original Cowrie with code handle with LLM
/LLM/GPT_3.5    Have files to handel command using gpt

# Files change in the original Cowrie
/cowrie/src/cowrie/shell/honeypot.py This change the code chunk in def lineReceived(self, line: str) -> None: 
Handle all the command.

    standardized_line = line.strip().lower()
    if standardized_line in ["exit", "logout", "shutdown", "reboot", "halt"]:
            self.protocol.terminal.loseConnection()
            return

        # Query GPT-4 for all commands
        gpt_response = query_gpt4_for_all_command(line)

        # Log the GPT-4 response
        if gpt_response:
            log.msg(eventid='cowrie.command.gpt4.response', output=gpt_response, 
                    format="GPT-4 response: %(output)s")

            self.protocol.terminal.write(gpt_response.encode() + "\n".encode())
            self.showPrompt()
            return  # Optionally return here if you don't want Cowrie to process the command further
        else:
            self.protocol.terminal.write("".encode())
            self.showPrompt()
            # Log when there is no GPT-4 response or continuing with Cowrie's processing
            log.msg(eventid="cowrie.command.gpt4.no_response", format="No GPT-4 response or continuing with Cowrie processing.")
            return
        

        tokens: list[str] = []

Handle unrecgnize command
you need to comment the handle all command code and then uncomment code below

    # while True:
        #     try:
        #         tokkie: str | None = self.lexer.get_token()
        #         # log.msg("tok: %s" % (repr(tok)))

        #         if tokkie is None:  # self.lexer.eof put None for mypy
        #             if tokens:
        #                 self.cmdpending.append(tokens)
        #             break
        #         else:
        #             tok: str = tokkie

        #         # For now, treat && and || same as ;, just execute without checking return code
        #         if tok == "&&" or tok == "||":
        #             if tokens:
        #                 self.cmdpending.append(tokens)
        #                 tokens = []
        #                 continue
        #             else:
        #                 self.protocol.terminal.write(
        #                     f"-bash: syntax error near unexpected token `{tok}'\n".encode()
        #                 )
        #                 break
        #         elif tok == ";":
        #             if tokens:
        #                 self.cmdpending.append(tokens)
        #                 tokens = []
        #                 continue
        #             else:
        #                 self.protocol.terminal.write(
        #                     f"-bash: syntax error near unexpected token `{tok}'\n".encode()
        #                 )
        #                 break
        #         elif tok == "$?":
        #             tok = "0"
        #         elif tok[0] == "(":
        #             cmd = self.do_command_substitution(tok)
        #             tokens = cmd.split()
        #             continue
        #         elif "$(" in tok or "`" in tok:
        #             tok = self.do_command_substitution(tok)
        #         elif tok.startswith("${"):
        #             envRex = re.compile(r"^\${([_a-zA-Z0-9]+)}$")
        #             envSearch = envRex.search(tok)
        #             if envSearch is not None:
        #                 envMatch = envSearch.group(1)
        #                 if envMatch in list(self.environ.keys()):
        #                     tok = self.environ[envMatch]
        #                 else:
        #                     continue
        #         elif tok.startswith("$"):
        #             envRex = re.compile(r"^\$([_a-zA-Z0-9]+)$")
        #             envSearch = envRex.search(tok)
        #             if envSearch is not None:
        #                 envMatch = envSearch.group(1)
        #                 if envMatch in list(self.environ.keys()):
        #                     tok = self.environ[envMatch]
        #                 else:
        #                     continue

        #         tokens.append(tok)
        #     except Exception as e:
        #         self.protocol.terminal.write(
        #             b"-bash: syntax error: unexpected end of file\n"
        #         )
        #         # Could run runCommand here, but i'll just clear the list instead
        #         log.msg(f"exception: {e}")
        #         self.cmdpending = []
        #         self.showPrompt()
        #         return

        # if self.cmdpending:
        #     self.runCommand()
        # else:
        #     self.showPrompt()
