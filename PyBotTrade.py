import requests

import json
import oandapyV20.exceptions
import oandapyV20.endpoints.accounts as accounts

from optparse import OptionParser


def connect_to_stream():
    """
    Environment              Description

    fxTrade (Live)              The live (real money) environment

    fxTrade Practice (Demo)     The demo (simulated money) environment

    """

    domainDict = {'live': 'stream-fxtrade.oanda.com',

                  'demo': 'stream-fxpractice.oanda.com'}

    # Replace the following variables with your personal values

    environment = "live"  # Replace this 'live' if you wish to connect to the live environment

    domain = domainDict[environment]

    access_token = 'bdfaebe33b86935cd5577b1724961d60-bd8934f1d7c3dfaba3028aeb71aa6a81'

    account_id = '101-004-15588736-001'

    instruments = 'EUR_USD,USD_JPY'

    try:
        s = requests.Session()

        url = "https://" + domain + "/v1/prices"

        headers = {'Authorization': 'Bearer ' + access_token,

                   # 'X-Accept-Datetime-Format' : 'unix'

                   }

        params = {'instruments': instruments, 'accountId': account_id}

        req = requests.Request('GET', url, headers=headers, params=params)

        pre = req.prepare()

        resp = s.send(pre, stream=True, verify=True)

        return resp

    except Exception as e:

        s.close()

        print("Caught exception when connecting to stream\n" + str(e))


def demo(displayHeartbeat):
    response = connect_to_stream()

    if response.status_code != 200:
        print(response.text)

        return

    for line in response.iter_lines(1):

        if line:
            try:
                line = line.decode('utf-8')
                msg = json.loads(line)
            except Exception as e:

                print("Caught exception when converting message into json\n" + str(e))

                return

            if "instrument" in msg or "tick" in msg or displayHeartbeat:
                print(line)


def main():
    usage = "usage: %prog [options]"

    parser = OptionParser(usage)

    parser.add_option("-b", "--displayHeartBeat", dest="verbose", action="store_true",

                      help="Display HeartBeat in streaming data")

    displayHeartbeat = False

    (options, args) = parser.parse_args()

    if len(args) > 1:
        parser.error("incorrect number of arguments")

    if options.verbose:
        displayHeartbeat = True

    demo(displayHeartbeat)


if __name__ == '__main__':
    main()
