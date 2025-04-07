from Models import load_main_model, load_analysis_model
from Utils import clean_command, run_command, log_session
from Config import load_system_prompt, load_system_prompt2
from MemoryManager import MemoryManager

def summarize_output(output: str) -> str:
    lines = output.strip().splitlines()
    important_lines = [line for line in lines if any(k in line.lower() for k in ["open", "vuln", "port", "user", "error", "root", "denied"])]
    if len(important_lines) < 3:
        important_lines = lines[:10]
    return "\n".join(important_lines)

def run_continuous_mode():
    target_ip = input("Enter the target IP address:\n>").strip()

    main_model = load_main_model()
    analysis_model = load_analysis_model()
    memory = MemoryManager()
    memory.load_memory()

    print(f"\n[+] Starting autonomous pentest for: {target_ip}...\n")
    main_prompt = load_system_prompt()
    analysis_prompt = load_system_prompt2()

    main_input = f"{main_prompt}\n\nTarget: {target_ip}\n\nBegin pentest. Return the first Linux command to execute:"

    try:
        with main_model.chat_session() as main_session, analysis_model.chat_session() as analysis_session:
            while True:
                raw_command = main_session.generate(main_input, max_tokens=50).strip()
                command = clean_command(raw_command)

                if not command or command.lower() in ["exit", "quit"]:
                    print("\n[-] No valid command or 'exit' detected. Ending session.")
                    break

                print(f"\n[>] Running Command: {command}")
                output = run_command(command)
                if isinstance(output, tuple):
                    output = output[0]

                print(f"\n[<] Output:\n{output}")
                log_session(f"Autonomous recon on {target_ip}", raw_command, command, output)

                summary = summarize_output(output)
                combined_text = f"Target: {target_ip}\nCommand: {command}\nOutput: {summary}"

                # Store to memory
                memory.add_memory(combined_text, command, summary, "")

                # Query memory to add context to analysis
                memory_context = memory.query_memory(command)
                context_snippets = "\n".join([f"Command: {m['command']}\nSummary: {m['summary']}" for m in memory_context])

                analysis_input = f"{analysis_prompt}\n\nTarget IP: {target_ip}\nCommand Run: {command}\nOutput:\n{summary}\n\nRecent Memory Context:\n{context_snippets}\n\nWhat does this tell us and what should be the next command?"

                analysis_output = analysis_session.generate(analysis_input, max_tokens=300).strip()
                print(f"\nAnalysis Insight:\n{analysis_output}")

                # Save full memory object
                memory.add_memory(combined_text, command, summary, analysis_output)

                main_input = f"{main_prompt}\n\nTarget: {target_ip}\nPrevious Analysis:\n{analysis_output}\n\nNext command:"

    except Exception as e:
        print(f"\n[!] Error occurred: {str(e)}")
    finally:
        memory.save_memory()
        print("\n[✓] Session ended and memory saved.")
