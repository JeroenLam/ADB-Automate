import os
from pathlib import Path

ADB_COMMAND = "../../platform-tools/adb"


class ADBWrapper:
    """
    A wrapper class for adb commands.
    """

    def __init__(self, adb_command: str | Path =ADB_COMMAND):
        """ Initializes the ADBWrapper.

        Args:
            adb_command (str | Path, optional): Path to the adb command that needs to be installed manually on the system. Defaults to ADB_COMMAND.

        Raises:
            FileNotFoundError: If the adb command is not found at the specified path.
            PermissionError: If the adb command is not executable.
        """
        self.adb_command = adb_command
        if not os.path.exists(adb_command):
            raise FileNotFoundError(
                f"ADB command not found at {adb_command}. Please ensure the path is correct."
            )
        if not os.access(self.adb_command, os.X_OK):
            raise PermissionError(
                f"ADB command at {self.adb_command} is not executable."
            )


    def run_command(self, command: str, device_id: str | None=None) -> str:
        """Run an ADB command.

        Args:
            command (str): Command to run.
            device_id (str | None, optional): Device ID from list_devices(). Defaults to None.

        Returns:
            str: stdout from the command.
        """
        # Add adb path
        full_command = f"{self.adb_command}"

        # Add device ID if provided
        if device_id:
            full_command += f" -s {device_id}"

        # Add the command to run
        full_command += f" {command}"

        # Capture the output
        output = os.popen(full_command).read()
        return output


    def list_devices(self) -> list[str]:
        """List connected devices.

        Returns:
            list[str]: List of device IDs connected to the ADB server.
        """        
        output = self.run_command("devices")
        devices = []
        for line in output.splitlines():
            if "\tdevice" in line:
                device_id = line.split("\t")[0]
                devices.append(device_id)
        return devices

    def dump_ui_xml(self, device_id: str | None=None) -> str:
        """Dump the UI hierarchy of the device.

        Args:
            device_id (str | None, optional): Device ID from list_devices(). Defaults to None.

        Returns:
            str: UI hierarchy in XML format.
        """
        output = self.run_command("exec-out uiautomator dump /dev/tty", device_id)
        # The output ends with "UI Hierarchy dumped to: /dev/tty", which we can remove
        xml_output = output[:-33]
        return xml_output
