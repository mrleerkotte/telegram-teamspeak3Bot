import ts3


class teamspeakActions:
    def getClients(TEAMSPEAK_QUERY_USER, TEAMSPEAK_QUERY_PASS, TEAMSPEAK_QUERY_SERVER):
        with ts3.query.TS3Connection(TEAMSPEAK_QUERY_SERVER) as ts3conn:
            # Note, that the client will wait for the response and raise a
            # **TS3QueryError** if the error id of the response is not 0.
            try:
                ts3conn.login(
                    client_login_name=TEAMSPEAK_QUERY_USER,
                    client_login_password=TEAMSPEAK_QUERY_PASS
                )
            except ts3.query.TS3QueryError as err:
                print("Login failed:", err.resp.error["msg"])
                exit(1)

            ts3conn.use(sid=1)

            # Each query method will return a **TS3QueryResponse** instance,
            # with the response.
            resp = ts3conn.clientlist()
            # print("Clients on the server:", resp.parsed)
            # print("Error:", resp.error["id"], resp.error["msg"])

            teamspeakClients = "*Online Clients*\n"

            if resp > 0:
                for client in resp.parsed:
                    if client['client_type'] == '0':
                        teamspeakClients = teamspeakClients + "_" + client['client_nickname'] + "_\n"

                return teamspeakClients
            else:
                return "No one online."

    def getBanlist(TEAMSPEAK_QUERY_USER, TEAMSPEAK_QUERY_PASS, TEAMSPEAK_QUERY_SERVER):
        with ts3.query.TS3Connection(TEAMSPEAK_QUERY_SERVER) as ts3conn:
            # Note, that the client will wait for the response and raise a
            # **TS3QueryError** if the error id of the response is not 0.
            try:
                ts3conn.login(
                    client_login_name=TEAMSPEAK_QUERY_USER,
                    client_login_password=TEAMSPEAK_QUERY_PASS
                )
            except ts3.query.TS3QueryError as err:
                print("Login failed:", err.resp.error["msg"])
                exit(1)

            ts3conn.use(sid=1)

            # Each query method will return a **TS3QueryResponse** instance,
            # with the response.
            try:
                resp = ts3conn.banlist()
                teamspeakBanlist = "*Banned Clients*\n"

                for ban in resp.parsed:
                    ip = ban['ip']
                    ip = ip.translate({ord(c): None for c in '\\'})

                    teamspeakBanlist = teamspeakBanlist + "_Name: " + ban['name'] + " IP: " + ip + \
                                       " By: " + ban['invokername'] + " Reason: " + ban['reason'] + "_\n"

                response = teamspeakBanlist
            except ts3.query.TS3QueryError as err:
                response = "No active bans."

            return response
