from instance.Client import Instance
from scripts.buy import buy


def fish(Client: Instance) -> bool:
    """
    The fish function is used to interact with the fish command

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    Client.send_message("pls fish")

    latest_message = Client.retreive_message("pls fish")

    if "Catch the fish" in latest_message["content"]:
        Client.log("DEBUG", "Detected catch the fish game.")

        level = (
            latest_message["content"]
            .split("\n")[1]
            .replace(latest_message["content"].split("\n")[1].strip(), "")
            .count("       ")
        )

        Client.interact_button(
            "pls fish",
            latest_message["components"][0]["components"][level]["custom_id"],
            latest_message,
        )

        return True

    if (
        latest_message["content"]
        == "You don't have a fishing pole, you need to go buy one. You're not good enough to catch them with your hands."
    ):
        Client.log(
            "DEBUG",
            "Account does not have item `fishing pole`. Buying fishing pole now.",
        )

        if (
            Client.Repository.config["auto buy"]
            and Client.Repository.config["auto buy"]["fishing pole"]
        ):
            return buy(Client, "fishing pole")
        else:
            Client.log(
                "WARNING",
                f"A fishing pole is required for the command `pls fish`. However, since {'auto buy is off for fishing poles,' if Client.Repository.config['auto buy']['enabled'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
            )
            return False

    if latest_message["content"] in [
        "Your fishing trip came up empty, shoes for dinner again tonight!",
        "Awh man, no fish wanted your rod today",
        "You cast out your line and sadly didn't get a bite",
    ]:
        Client.log("DEBUG", f"Found nothing from the `pls fish` command.")
    else:
        item = (
            latest_message["content"]
            .replace("You cast out your line and brought back 1 ", "")
            .split("<:")[0]
            .split("<a:")[0]
        ).strip()

        Client.log("DEBUG", f"Received 1 {item.lower()} from the `pls fish` command.")

        Client._update_items("pls fish", item)

    return True
