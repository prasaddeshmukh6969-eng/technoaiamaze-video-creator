import sys
import os
sys.path.append(os.path.join(os.getcwd(), "server"))

log_file = "import_debug.log"

with open(log_file, "w", encoding="utf-8") as log:
    try:
        print("Importing v1_generation...", file=log)
        from routers import v1_generation
        print("Import SUCCESS", file=log)
    except Exception as e:
        print(f"Import FAILED: {e}", file=log)
        import traceback
        traceback.print_exc(file=log)
