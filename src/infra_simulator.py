import resources as resources
from machine import Machine
import logging
from pydantic import ValidationError
import re
import file_utils

# Configure logging
logging.basicConfig(filename='./logs/provisioning.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def get_user_input():
    machine_data = {}
    # Get new machine
    name = None
    while True:
        name = input("Enter machine name: ").strip()
        logging.info(f"User entered machine name: {name}")
        if len(name):
            break
        logging.warning("Machine name is empty")
        print("You not entered machine name. Please try again")
    machine_data["name"] = name

    # Get OS
    os_to_display = " / ".join(resources.os)
    os = None
    while True:
        os = input(f"Enter OS (e.g. {os_to_display}): ").strip()
        # I assume that OS in lowercase and starts with capital letter
        os = os.lower().capitalize()
        logging.info(f"User entered OS: {os}")
        if os in resources.os:
            break
        logging.warning(f"OS {os} not available")
        print("OS not available. Please try again")
    machine_data["os"] = os

    # Get number CPU's
    cpu = None
    while True:
        cpu = input(
            f"Enter number of CPU's (Any integer value up to {resources.cpu}): ").strip()
        logging.info(f"User entered number of CPU's: {cpu}")
        if cpu.isnumeric():
            break
        logging.warning("Number of CPU's is not a number")
        print("It should be a number. Please try again.")
    machine_data["cpu"] = int(cpu)

    # Get RAM capacity
    ram = None
    while True:
        ram = input("Enter RAM capacity in GiB : ").strip()
        logging.info(f"User entered RAM capacity: {ram}")
        if re.match(r"^\d+(\.\d+)?$", ram):
            break
        logging.warning("Invalid RAM capacity")
        print("It should be a number. Please try again.")
    machine_data["ram"] = float(ram)

    return machine_data


logging.info("Script started!")
machines = []
while True:
    try:
        machine_data = get_user_input()
        machine = Machine(**machine_data)
        machines.append(machine)
    # Handle validation errors
    except ValidationError as err:
        errors = err.errors()
        errors = map(lambda e: e["loc"][0], errors)
        *errors, = map(str.upper, errors)
        errors = ", ".join(errors)
        print("Values of {errors} out valid range")
        logging.error(f"Got {err.error_count} validation Errors {errors}")
        continue
    # Handle ValueError:
    except ValueError:
        logging.error("Got invalid value")
        print("One or more parameters are invalid.\nPlease Try again.")
        continue
    # Handle unexpected errors
    except Exception as err:
        print(err)
        print("Something went wrong.\nPlease try again")
        continue
    get_next = input(
        "Add another Machine?\nPress Y for yes: ").lower().strip()
    if not get_next == "y":
        break


old_machines = []
try:
    logging.info("Loading old configurations")
    old_machines = file_utils.read()
except Exception as err:
    logging.error("Configuration not loaded")
    logging.error("Reason of error is " + err)


*new_machines, = map(lambda m: m.to_dict(), machines)
all_machines = [*old_machines, *new_machines]
# Save machines configuration
try:
    logging.info("Saving configuration")
    file_utils.write(all_machines,"./configs/instances.json")
except Exception as err:
    logging.error("Configuration not saved")
    logging.error("Reason of error is " + err)

logging.info("Script ended!")
