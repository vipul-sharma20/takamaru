CONFIG_FILE = "../.takamaru.conf"

SUBREDDITS = ["python", "programming", "coolgithubprojects"]

# list of query tuples (combination of keywords which should appear together)
QUERIES = [("python 3.6",), ("tensorflow",), ("django",)]

REDDIT_RECIPIENTS = ["vipul.sharma20@gmail.com"]

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_TEMPLATE = """
<html>
    <table style="width:100%">
        {rows}
    </table>
</html>
"""

TABLE_COLUMNS = "<td width={width}>{content}</td>"
TABLE_ROWS = "<tr>{content}</tr>"
ANCHOR_TAG = "<a href={href}>{content}</a>"

ZEBPAY_URL = "http://zebpay.com/"
BUY_THRESHOLD = 289000
SELL_THRESHOLD = 300000
ZEBPAY_RECIPIENTS = ["vipul.sharma20@gmail.com", "vipul@driveu.in"]
