import ts3


class TeamspeakActions:
    @staticmethod
    def get_clients(teamspeak_query_user, teamspeak_query_pass, teamspeak_query_server):
        with ts3.query.TS3Connection(teamspeak_query_server) as ts3conn:
            # Note, that the client will wait for the response and raise a
            # **TS3QueryError** if the error id of the response is not 0.
            try:
                ts3conn.login(
                    client_login_name=teamspeak_query_user,
                    client_login_password=teamspeak_query_pass
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

            teamspeak_clients = ""

            for client in resp.parsed:
                if client['client_type'] == '0':
                    teamspeak_clients = teamspeak_clients + "_" + client['client_nickname'] + "_\n"

            if teamspeak_clients == "":
                teamspeak_clients = "*No one online.\n*"
                return teamspeak_clients
            else:
                return teamspeak_clients

    @staticmethod
    def get_bans(teamspeak_query_user, teamspeak_query_pass, teamspeak_query_server):
        with ts3.query.TS3Connection(teamspeak_query_server) as ts3conn:
            # Note, that the client will wait for the response and raise a
            # **TS3QueryError** if the error id of the response is not 0.
            try:
                ts3conn.login(
                    client_login_name=teamspeak_query_user,
                    client_login_password=teamspeak_query_pass
                )
            except ts3.query.TS3QueryError as err:
                print("Login failed:", err.resp.error["msg"])
                exit(1)

            ts3conn.use(sid=1)

            # Each query method will return a **TS3QueryResponse** instance,
            # with the response.
            try:
                resp = ts3conn.banlist()
                teamspeak_bans = "*Banned Clients*\n"

                for ban in resp.parsed:
                    ip = ban['ip']
                    ip = ip.translate({ord(c): None for c in '\\'})

                    teamspeak_bans = teamspeak_bans + "_Name: " + ban['name'] + " IP: " + ip + \
                                       " By: " + ban['invokername'] + " Reason: " + ban['reason'] + "_\n"

                response = teamspeak_bans
            except ts3.query.TS3QueryError as err:
                response = "*No active bans.*\n"

            return response
