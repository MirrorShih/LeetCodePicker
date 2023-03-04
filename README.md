# LeetCodePicker

LeetCodePicker is a Python project that selects LeetCode problems randomly and updates them on [hackmd.io](https://hackmd.io/) weekly. 
The project has a unique feature that it does not select LeetCode premium problems, 
and users can customize the number and difficulty of problems by modifying the configuration. 
LeetCodePicker also ensures that it does not select problems that have already been chosen. 
The project is available on GitHub and can be used by forking the repository.

## Usage

To use LeetCodePicker, you need to first fork the repository to your GitHub account. 
Then, you need to set up the following environment variables as [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets):

- `NOTE`: The hackmd note ID to update. You can find the note ID in the URL of your note.
- `TOKEN`: Your hackmd API token. You can generate a token by going to your account settings and clicking "Create API token" under "API".
- `WEBHOOK`: (Optional)The webhook URL (without "https://discord.com/api/webhooks/" ) to trigger when the LeetCodePicker action is completed. This is useful for sending notifications to Discord.

If you want to receive notifications on a Discord channel when the LeetCodePicker action is completed, 
you can set up a Discord webhook and add the webhook URL to the `WEBHOOK` secret.

Next, you can customize the configuration by modifying the `config` file. 
The file contains the following configuration options:

- easy: The number of easy questions to select.
- medium: The number of medium questions to select.
- hard: The number of hard questions to select.

If you want to clear the history of selected questions, you need to empty the contents of the `done.txt` file. 
This file contains the list of questions that have already been selected.

If you want to customize the frequency of running LeetCodePicker, 
you can modify the cron schedule in the main.yml file located in the .github/workflows directory.

## Contributing

If you find any issues with the project, feel free to create an issue on the repository. 
You are also welcome to contribute to the project by submitting a pull request.