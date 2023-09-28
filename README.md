# Tool thingy that applies a label to tasks under a colored parent project
This tool will apply a label (like your company name) to tasks that are beneath a parent Todoist Project of a specific color (Like your company's color)

# Set up
1. Clone this repo
2. Run make_env.sh
3. Make a copy of config.json.TEMPLATE and name it config.json
4. Configure it
5. NEVER EVER EVER EVER put your API key or other secrets under version control.  EVER!  (I'm looking at you, config.json)
6. Set up a cron tab to run this script periodically.  It might look kike this:  `*/15 * * * * cd ~/projects/todoist-project-color-label && bash go.sh > todoist-project-color-label.log 2>&1`