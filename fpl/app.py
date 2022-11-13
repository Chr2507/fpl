import streamlit as st
import plotly_express as px

from fpl.api_calls import get_combined_manager_history
    
managers_dict = {
    "Chistian": 1302722,
    "Hans-Martin": 2584139,
    "Andreas": 4306388,
}

df = get_combined_manager_history(managers_dict=managers_dict)

df = df.drop(columns=["rank_sort"])
df["value"] = df["value"]/10
df["bank"] = df["bank"]/10

df = df.rename(columns={
    "event":"gameweek",
    "rank":"gw_rank",
    "event_transfers":"transfers",
    "event_transfers_cost":"transfer_cost",
    "value":"team_value",
    "bank":"money_in_bank",
    "points_on_bench":"points_benched"
    })


df["total_points_benched"] = df.groupby(["manager"])["points_benched"].transform("cumsum")
df["total_transfers"] = df.groupby(["manager"])["transfers"].transform("cumsum")
df["total_transfer_cost"] = df.groupby(["manager"])["transfer_cost"].transform("cumsum")


st.header("Interaktiv graf for FPL 2022/23")
st.text("Fra drop down menuen kan du vælge mellem en række variable, der beskriver \nudviklingen henover sæsonen.")

y_vals = [col for col in df.columns if col != "gameweek"]
y_axis_val = st.selectbox("Vælg variabel til y-aksen:", options=y_vals)


plot = px.line(
    df, 
    x="gameweek", 
    y=y_axis_val,
    color="manager",
    markers=True
    )

reverse_vals = ["gw_rank","rank_sort","overall_rank"]
if y_axis_val in reverse_vals:
    plot.update_yaxes(
        # autorange="reversed",
        range=[10880000,0])

plot.update_layout(
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 1,
        dtick = 1
    )
)

st.plotly_chart(plot)