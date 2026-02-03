
import os
import subprocess
import sys
import shutil
import json
import backpack
print(f"DEBUG: backpack package location: {backpack.__file__}")

from backpack.agent_lock import AgentLock

def setup_test_env(dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.makedirs(dir_name)
    return dir_name

def create_agent_script(path, var_name):
    with open(path, "w") as f:
        f.write(f"""
import os
import sys
val = os.environ.get("{var_name}")
if val:
    print(f"FOUND: {{val}}")
else:
    print("NOT FOUND")
""")

def test_cloud_run():
    test_dir = "test_cloud_env"
    setup_test_env(test_dir)
    original_cwd = os.getcwd()
    os.chdir(test_dir)

    try:
        # 1. Initialize agent.lock
        lock = AgentLock("agent.lock")
        # Scenario A: Key in Environment
        lock.create(
            {"TEST_ENV_KEY": "placeholder_test_env_key"}, 
            {"system_prompt": "test", "tone": "test"}
        )
        
        agent_script = "agent_env.py"
        create_agent_script(agent_script, "TEST_ENV_KEY")

        print("--- Test Case 1: Cloud Mode + Key in Environment ---")
        # Run backpack run with AGENT_MASTER_KEY set and Key in Env
        env = os.environ.copy()
        env["AGENT_MASTER_KEY"] = "default-key"
        env["TEST_ENV_KEY"] = "secret_from_env"
        
        # Ensure PYTHONPATH is set in the subprocess environment
        if "PYTHONPATH" not in env:
            print("WARNING: PYTHONPATH not in env, setting to src")
            env["PYTHONPATH"] = os.path.abspath(os.path.join(original_cwd, "src"))
        else:
            print(f"DEBUG: PYTHONPATH is {env['PYTHONPATH']}")
        
        # Debug: Check where backpack.cli comes from in the subprocess
        debug_cmd = [sys.executable, "-c", "import backpack.cli; print(backpack.cli.__file__)"]
        subprocess.run(debug_cmd, env=env)

        # We need to run the backpack cli. 
        # Since we are in the same repo, we can run `python -m backpack.cli run ...`
        cmd = [sys.executable, "-m", "backpack.cli", "run", agent_script]
        
        # We expect NO prompt. If there is a prompt, it will hang or fail reading stdin.
        # We set input to empty to ensure it fails if it prompts.
        result = subprocess.run(
            cmd, 
            env=env, 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        
        if result.returncode != 0:
            print("FAILED: Process exited with error")
            print(result.stderr)
        else:
            if "FOUND: secret_from_env" in result.stdout:
                print("PASSED: Key found from environment")
            else:
                print("FAILED: Key not found or wrong value")
                print(result.stdout)

        # Scenario B: Key in Lock File (Encrypted Portability)
        print("\n--- Test Case 2: Cloud Mode + Key in Lock File ---")
        # Re-create lock with REAL value
        lock.create(
            {"TEST_LOCK_KEY": "secret_embedded_in_lock"}, 
            {"system_prompt": "test", "tone": "test"}
        )
        
        agent_script_lock = "agent_lock.py"
        create_agent_script(agent_script_lock, "TEST_LOCK_KEY")
        
        env = os.environ.copy()
        env["AGENT_MASTER_KEY"] = "default-key"
        if "PYTHONPATH" not in env:
             env["PYTHONPATH"] = os.path.abspath(os.path.join(original_cwd, "src"))

        # Ensure it's NOT in env
        if "TEST_LOCK_KEY" in env:
            del env["TEST_LOCK_KEY"]
            
        cmd = [sys.executable, "-m", "backpack.cli", "run", agent_script_lock]
        result = subprocess.run(
            cmd, 
            env=env, 
            capture_output=True, 
            text=True, 
            timeout=5
        )

        if result.returncode != 0:
            print("FAILED: Process exited with error")
            print(result.stderr)
        else:
            if "FOUND: secret_embedded_in_lock" in result.stdout:
                print("PASSED: Key injected from lock file")
            else:
                print("FAILED: Key not found or wrong value")
                print(result.stdout)

    finally:
        os.chdir(original_cwd)
        # shutil.rmtree(test_dir) # Keep for debugging if needed

if __name__ == "__main__":
    test_cloud_run()
