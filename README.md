# BurnInTest Plugin Python Interface (`burnintest-plugin`)

A simple wrapper for interfacing with PassMark's BurnInTest plugin system. 

BurnInTest allows you to integrate custom testing tools via a shared memory interface. This package abstracts away the underlying `ctypes` and `multiprocessing.shared_memory` boilerplate, giving you a simple, object-oriented API to communicate statuses, log errors, and track test cycles directly from Python.

## Features

* **Context Manager Support:** Automatically handles shared memory cleanup and safe exits.
* **Built-in Enums:** Statuses and error severities are mapped to standard Python Enums (`PluginStatus`, `ErrorSeverity`).
* **Safe Encoding:** Automatically handles UTF-8 encoding and string truncation to prevent buffer overflows in the underlying C-struct.
* **State Tracking:** Easily update cycles, duty cycles, read/write/verify operations, and error counts.

## Installation

```bash
pip install burnintest-plugin
```

## Quick Start

When BurnInTest launches a plugin, it passes a unique shared memory key as the first entry in argv. You use this key to initialize the `BitInterface`.

Below is an example of a simple plugin that verifies hardware states and communicates its progress back to the BurnInTest dashboard.

``` python
import sys
import time
from burnintest_plugin import BitInterface, PluginStatus, ErrorSeverity

def main():
    # BurnInTest passes the shared memory key as a command line argument
    mem_key = sys.argv[0]
    if not mem_key.startswith("BIT_PLUGIN_INT"):
        print("No BIT shared memory key found... Aborting!")
        sys.exit(1)

    # Use the context manager for clean shared memory cleanup
    with BitInterface(key=mem_key, window_title="Custom BIT Plugin") as bit:
        
        bit.set_status(PluginStatus.PLUGIN_STARTUP, "Initializing hardware SDK...")
        time.sleep(1)

        # Simulating a testing loop (e.g., verifying GPIO/DIO or memory states)
        bit.set_status(PluginStatus.PLUGIN_READING, "Verifying module states...")

        for i in range(10):
            # Always check if the user has stopped the test in the BurnInTest UI
            if not bit.test_running:
                break

            # Simulate a read operation
            bit.read_operations += 1
            time.sleep(0.5)

            # Simulate catching a minor hardware anomaly (e.g., a recoverable bit flip)
            if i == 5:
                bit.log_message(ErrorSeverity.ERRORWARNING, "Minor state mismatch detected, retrying...")
                # Note: log_message automatically increments bit.error_count for severities > WARNING

            # Update metrics
            bit.verify_operations += 1
            bit.cycle += 1

        bit.set_status(PluginStatus.PLUGIN_CLEANUP, "Cleaning up resources...")

if __name__ == "__main__":
    main()
```

## Usage Notes

* **Blocking vs Non-Blocking:** Methods like `set_status` and `log_message` have an optional `wait` boolean parameter. When `True`, the Python script will block until BurnInTest acknowledges the update. If back to back calls are made, the second call will always wait for the first to be acknowledged.
* **Pre-Testing:** If you are using this script as a Pre-Test plugin, you can call `bit.set_pretest_complete()` to signal to BurnInTest that it should proceed with the main testing phase.
