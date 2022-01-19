import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_tables(urls, link=False):
    """Returns a dataframes list with the tables of the different groups.

    Keyword arguments:
        urls -- list with urls of the different groups
        link -- indicates whether you want to include the url of every team in the dataframe
            (default False)."""

    # Declare header variable with browsers info
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/47.0.2526.106 Safari/537.36'}
    tables_list = []  # Save results in a list

    try:
        # Create BeautifulSoup objects from our responses
        for i, url in enumerate(urls):
            response = requests.get(url, headers=headers)
            url_bs = BeautifulSoup(response.content, 'html.parser')

            # Lists
            header = []
            datos = []

            # The find_all() method returns the tags with the required information.
            tags_header = url_bs.find_all("div", {"class": "classificationHeadingItem"})
            tags_data = url_bs.find_all("div",
                                        {"class": ["classificationItemOddWrapper", "classificationItemEvenWrapper"]})
            tags_link = url_bs.find_all("a", {"class": "classificationTeam"})

            # Extract headers, teams, goals and url links.
            for tag_header in tags_header:
                header.append(tag_header.text)
            header.insert(0, 'Equipo'), header.insert(0, 'POS')
            header = header[:-1]

            for tag_data in tags_data:
                datos.append(tag_data.text)

            links_lst = []
            for tag_link in tags_link:
                links_lst.append('https://www.futboleras.es' + tag_link.get('href'))

            # Format and put the data into a dataframe.
            df = pd.DataFrame([sub.split('    ') for sub in datos])
            df.drop(df.columns[[0, 10, 11]], axis=1, inplace=True)
            splitcol = df[2].str.split('  ', 2, expand=True)

            # Add the points, group and url links of each team.
            df.insert(1, 'Equipo', splitcol[1]), df.insert(2, 'PTOS', splitcol[2])
            del (df[2])
            df.columns = header
            df.insert(2, 'Grupo', i + 1)
            if link:
                df['Link'] = links_lst
            tables_list.append(df)

        return tables_list

    except Exception:
        print('Enter a valid url list.')


def general_table(tables_list):
    """Returns the general table with all the teams.

    Keyword arguments:
        table_list -- list with all tables stored in dataframes"""

    # Concatenate all dataframes.
    df = pd.concat(tables_list, axis=0)

    # Transform the columns to manipulate to integers.
    df[['PTOS', 'PJ', 'POS', 'PG', 'PE', 'PP', 'GF', 'GC', 'DG']] = \
        df[['PTOS', 'PJ', 'POS', 'PG', 'PE', 'PP', 'GF', 'GC', 'DG']].astype('int')
    # Add the points per match.
    df['PPP'] = (df.PTOS / df.PJ).round(2)
    # Sorted table
    df = df.sort_values(by=['PPP'], ascending=False)

    return df


def top_scorers(urls, n=10, group=False):
    """Returns a list with the dataframes of the top scorers for each championship group.

    Keyword arguments:
        urls -- list with urls of the different top scorers groups.
        n -- integer indicating the number of top scorers showed.
            (default 10).
        group -- integer indicating the dataframe group showed (default False returns
            the dataframes list)."""

    # Declare header variable with browsers info
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/47.0.2526.106 Safari/537.36'}
    scorers_list = []  # Save results in a list

    # Create BeautifulSoup objects from our responses
    for i, url in enumerate(urls):
        response = requests.get(url, headers=headers)
        url_bs = BeautifulSoup(response.content, 'html.parser')

        # Lists
        jug = []
        equipo = []
        goles = []

        # The find_all() method returns the tags with the required information.
        tags_jug = url_bs.find_all("a", {"class": "scorersItemInfoPlayer"})
        tags_equipo = url_bs.find_all("a", {"class": "scorersItemInfoTeam"})
        tags_goles = url_bs.find_all("div", {"class": "scorersItemGoalsValue"})

        # Extract players, teams, goals and url links.
        for tag_jug in tags_jug:
            jug.append(tag_jug.text)
        for tag_equipo in tags_equipo:
            equipo.append(tag_equipo.text)
        for tag_goles in tags_goles:
            goles.append(tag_goles.text)

        # Format and put the data into a dataframe.
        df = pd.DataFrame({"Jugadora": jug[:20], "Equipo": equipo[:20], "Goles": goles[:20]})
        df.insert(2, 'Grupo', i + 1)
        scorers_list.append(df)

    if n:
        if group:
            return scorers_list[group - 1][:n]
        else:
            scorers_list2 = []
            for df in scorers_list:
                scorers_list2.append(df[:n])
            return scorers_list2
    if not n:
        if group:
            return scorers_list[group - 1]
        else:
            return scorers_list


def general_top_scorers(scorers_list, n=10):
    """Returns a dataframe with the top scorers of the entire championship.

    Keyword arguments:
        scorers_list -- list with the dataframes top scorers.
        n -- integer (default 10 top scorers).
    """
    # Concatenate all dataframes.
    df = pd.concat(scorers_list, axis=0)
    # Transform goals column into integer
    df.Goles = df.Goles.astype('int')
    # Sorted table
    df = df.sort_values(by=['Goles'], ascending=False)

    return df[:n]


def relegated_teams(df):
    """Returns a list with teams who are relegated to lower category.
    The last two teams from each league relegated.

    Keyword arguments:
        df -- dataframe with the championship table"""

    relegation_list = []

    # iterate over each row and check if its a relegation position.
    for i, row in df.iterrows():
        if row['POS'] > 12:
            relegation_list.append(row['Equipo'])

    return relegation_list


def promoted_teams(df):
    """Returns a list with teams who are promoted to upper category.
    The first two teams from each are promoted.
    The best 4 third teams of the entire championship are promoted.

    Keyword arguments:
        df -- dataframe with the championship table"""

    promotion_list = []
    promotion_thirds = []

    # iterate over each row and check if its a promotion position.
    for i, row in df.iterrows():
        if row['POS'] < 3:
            promotion_list.append(row['Equipo'])
        if row['POS'] == 3:
            promotion_thirds.append(row['Equipo'])
    # add the third position teams promoted to the promotion list.
    promotion_list.extend(promotion_thirds[:4])

    return promotion_list


def team_goals(df, var='GF', reverse=False, n=5):
    """Returns a dataframe with the top or bottom teams from goals scored goals received or
     difference in goals.

    Keyword arguments:
        df -- dataframe with the championship table.
        var -- string with the variable to analyze. Only 'GF', 'GC' or 'DG' are accepted (default 'GF').
        reverse -- bool indicating if top or bottom teams are shown.
        n -- integer indicating the number of teams are shown.
            (default 10)."""

    d = {}  # store results in a dict.

    # iterate through rows according to the entered variable if you want to show the best teams.
    # store the results in d.
    if not reverse:
        if var == 'GC':
            for i, row in df.sort_values(by=['GC'], ascending=True)[:n].iterrows():
                d[row['Equipo']] = [row['GC'], row['Grupo']]
        if var == 'GF':
            for i, row in df.sort_values(by=['GF'], ascending=False)[:n].iterrows():
                d[row['Equipo']] = [row['GF'], row['Grupo']]
        if var == 'DG':
            for i, row in df.sort_values(by=['DG'], ascending=False)[:n].iterrows():
                d[row['Equipo']] = [row['DG'], row['Grupo']]

    # iterate through rows according to the entered variable if you want to show the worst teams.
    # store the results in d.
    if reverse:
        if var == 'GC':
            for i, row in df.sort_values(by=['GC'], ascending=False)[:n].iterrows():
                d[row['Equipo']] = [row['GC'], row['Grupo']]
        if var == 'GF':
            for i, row in df.sort_values(by=['GF'], ascending=True)[:n].iterrows():
                d[row['Equipo']] = [row['GF'], row['Grupo']]
        if var == 'DG':
            for i, row in df.sort_values(by=['DG'], ascending=True)[:n].iterrows():
                d[row['Equipo']] = [row['DG'], row['Grupo']]

    # return a dataframe from d.
    return pd.DataFrame.from_dict(d, orient='index', columns=[var, 'Grupo'])
