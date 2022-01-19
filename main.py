
from Utils import get_tables, general_table, top_scorers, general_top_scorers, \
    promoted_teams, relegated_teams, team_goals

# store urls in lists
table_urls = ['https://www.futboleras.es/primera-nacional/grupo-g1.html',
              'https://www.futboleras.es/primera-nacional/grupo-g2.html',
              'https://www.futboleras.es/primera-nacional/grupo-g3.html',
              'https://www.futboleras.es/primera-nacional/grupo-g4.html',
              'https://www.futboleras.es/primera-nacional/grupo-g5.html',
              'https://www.futboleras.es/primera-nacional/grupo-g6.html',
              'https://www.futboleras.es/primera-nacional/grupo-g7.html']

scorers_urls = ['https://www.futboleras.es/primera-nacional/goleadoras-grupo-g1.html',
                'https://www.futboleras.es/primera-nacional/goleadoras-grupo-g2.html',
                'https://www.futboleras.es/primera-nacional/goleadoras-grupo-g3.html',
                'https://www.futboleras.es/primera-nacional/goleadoras-grupo-g4.html',
                'https://www.futboleras.es/primera-nacional/goleadoras-grupo-g5.html',
                'https://www.futboleras.es/primera-nacional/goleadoras-grupo-g6.html',
                'https://www.futboleras.es/primera-nacional/goleadoras-grupo-g7.html']


print('Group 3 table')
tables_lst = get_tables(table_urls)
print(tables_lst[2])
print(' ')
print('General table with the 10 best teams in the category for all groups')
df_tab = general_table(tables_lst)
print(df_tab.head(10))
print(' ')
print('General table with the 10 worst teams in the category for all groups')
print(df_tab.tail(10))
print(' ')
print('Overall ranking of the third ranked (ascending to the top 4)')
print(df_tab[df_tab.POS == 3])
print(' ')
print('3 top scorers from group 4')
print(top_scorers(scorers_urls, n=3, group=4))
print(' ')
print('15 top scorers in the championship for all groups')
print(general_top_scorers(top_scorers(scorers_urls), 15))
print(' ')
print('Teams that are promoted')
print(promoted_teams(df_tab))
print(' ')
print('Teams that are relegated')
print(relegated_teams(df_tab))
print(' ')
print('Top scoring teams in the category')
print(team_goals(df_tab))
print(' ')
print('Least thrashed teams in the category')
print(team_goals(df_tab, var='GC'))
print(' ')
print('Teams with the best goal difference')
print(team_goals(df_tab, var='DG'))
print(' ')
print('Most scored teams')
print(team_goals(df_tab, var='GC', reverse=True))
print(' ')
print('Less goal-scoring teams')
print(team_goals(df_tab, var='GF', reverse=True))
print(' ')
print('Teams with the worst goal difference')
print(team_goals(df_tab, var='DG', reverse=True))
