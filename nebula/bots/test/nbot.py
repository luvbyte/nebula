
# Testing charts
def on_command(command: str, files, bot):
    if command == "bar":
        bot.print_chart({
            "type": "bar",
            "data": {
                "labels": ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
                "datasets": [{
                    "label": "# of Votes",
                    "data": [12, 19, 3, 5, 2, 3],
                    "borderWidth": 1
                }]
            },
            "options": {
                "scales": {
                    "y": { "beginAtZero": True }
                }
            }
        })

    elif command == "line":
        bot.print_chart({
            "type": "line",
            "data": {
                "labels": ["Jan", "Feb", "Mar", "Apr", "May"],
                "datasets": [{
                    "label": "Revenue ($k)",
                    "data": [5, 8, 12, 15, 22],
                    "borderWidth": 2,
                    "fill": False
                }]
            }
        })

    elif command == "pie":
        bot.print_chart({
            "type": "pie",
            "data": {
                "labels": ["Chrome", "Firefox", "Safari", "Edge"],
                "datasets": [{
                    "label": "Browser Market Share",
                    "data": [60, 15, 10, 15]
                }]
            }
        })

