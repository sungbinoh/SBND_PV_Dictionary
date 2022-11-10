import os
import psycopg2
from psycopg2 import Error

connection = psycopg2.connect(user="sungbino",
                                  password="",
                                  host="sbnd-db01",
                                  port="5434",
                                  database="sbnd_online_prd")

cursor = connection.cursor()
cursor.execute("set search_path to dcs_prd;")

cmd_check_chan_grp = "select grp_id,name,descr,eng_id from chan_grp order by grp_id;"
cursor.execute(cmd_check_chan_grp)
chan_grp = cursor.fetchall()
#print(chan_grp)

out_file = "PV_dictionary.tex"
f = open(out_file,'w')

group_names = {}
index_group = 0
## == List of systems
f.write(
'''
\\begin{table}[ptb]
\centering
\\begin{tabular}{c | c c}
\hline
Group ID & System name & Description \\\ \n
\hline
'''
)
for grp in chan_grp:
    grp_id = grp[0]
    name = grp[1]
    name = name.replace("_", "\_")
    descr = grp[2]
    group_names[grp_id] = name
    index_group = index_group + 1
    #print(str(grp_id) + "\t" + name + "\t" + descr)
    f.write(str(grp_id) + " & " + name + " & " + descr + "\\\ \n")
f.write(
'''
\hline
\end{tabular}
\caption{List of systems}
\label{tab:system_list}
\end{table}
'''
)

print(group_names) 
## == List of PVs for all systems
for i in range(1, 16):
    if i == 10:
        continue

    cmd_check_channel = "select channel_id,name,descr,smpl_mode_id,smpl_val,smpl_per from channel where grp_id=" + str(i) + " order by channel_id;"
    cursor.execute(cmd_check_channel)
    channel = cursor.fetchall()
    f.write(
'''
\\begin{center}
\\begin{longtable}{c | c c c c }
'''
)
    f.write("\caption{" + group_names[i] + " : PV lists}\n")
    f.write("\label{tab:" + group_names[i] + "_PV_list} \\\ \n")

    f.write(
'''

\hline \multicolumn{1}{|c|}{\\textbf{PV Name}} & \multicolumn{1}{c|}{\\textbf{Description}} & \multicolumn{1}{c|}{\\textbf{smpl\_mode\_id}} & \multicolumn{1}{c|}{\\textbf{smpl\_val}} & \multicolumn{1}{c|}{\\textbf{smpl\_per}} \\\ \hline \endfirsthead

\multicolumn{5}{c}%
{{\\bfseries \\tablename\ \\thetable{} -- continued from previous page}} \\\
\multicolumn{1}{|c|}{\\textbf{PV Name}} &
\multicolumn{1}{c|}{\\textbf{Description}} &
\multicolumn{1}{c|}{\\textbf{smpl\_mode\_id}} &
\multicolumn{1}{c|}{\\textbf{smpl\_val}} &
\multicolumn{1}{c|}{\\textbf{smpl\_per}} \\\ \hline
\endhead

\hline \multicolumn{5}{|r|}{{Continued on next page}} \\\ \hline
\endfoot

\hline \hline
\endlastfoot

'''
)

    for PV in channel:
        channel_id = PV[0]
        name = PV[1]
        descr = PV[2]
        smpl_mode_id = PV[3]
        smpl_val = PV[4]
        smpl_per = PV[5]
        if descr is None:
            descr = "-"
        name = name.replace("_", "\_")

        ## Exception handlings
        if i == 5:
            if "location" in name:
                descr = "Global Coordinates"

        f.write(name + " & " +descr + " & ")
        f.write(str(smpl_mode_id))
        f.write(" & ")
        f.write(str(smpl_val))
        f.write(" & ")
        f.write(str(smpl_per))
        f.write("\\\ \n")

    f.write(
'''
\hline
\end{longtable}
\end{center}

'''
)
