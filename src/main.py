# Must precede any llm module imports
from langtrace_python_sdk import langtrace
import os
from dotenv import load_dotenv

langtrace.init(api_key=os.environ.get("LANGTRACE_API_KEY"))
from crewai import Crew
from tasks import MeetingPrepTasks
from agents import MeetingPrepAgents


def main():
    load_dotenv()

    print("## Welcome to the Meeting Prep Crew")
    print("-------------------------------")
    meeting_participants = input(
        "What are the emails for the participants (other than you) in the meeting?\n"
    )
    meeting_context = input("What is the context of the meeting?\n")
    meeting_objective = input("What is your objective for this meeting?\n")

    tasks = MeetingPrepTasks()
    agents = MeetingPrepAgents()

    # create agents
    research_agent = agents.research_agent()
    industry_analysis_agent = agents.industry_analysis_agent()
    meeting_strategy_agent = agents.meeting_strategy_agent()
    summary_and_briefing_agent = agents.summary_and_briefing_agent()

    # create tasks
    research_task = tasks.research_task(
        research_agent, meeting_participants, meeting_context
    )
    industry_analysis_task = tasks.industry_analysis_task(
        industry_analysis_agent, meeting_participants, meeting_context
    )
    meeting_strategy_task = tasks.meeting_strategy_task(
        meeting_strategy_agent, meeting_context, meeting_objective
    )
    summary_and_briefing_task = tasks.summary_and_briefing_task(
        summary_and_briefing_agent, meeting_context, meeting_objective
    )

    # context within Crewai framework is how you define passing data
    # from one task to another. In this case, the meeting strategy task
    # requires data from the reserarch task and the analysis task
    meeting_strategy_task.context = [research_task, industry_analysis_task]
    # to create a summary, you need all outputs from all the tasks
    summary_and_briefing_task.context = [
        research_task,
        industry_analysis_task,
        meeting_strategy_task,
    ]

    crew = Crew(
        agents=[
            research_agent,
            industry_analysis_agent,
            meeting_strategy_agent,
            summary_and_briefing_agent,
        ],
        tasks=[
            research_task,
            industry_analysis_task,
            meeting_strategy_task,
            summary_and_briefing_task,
        ],
    )

    result = crew.kickoff()

    print(result)


if __name__ == "__main__":
    main()
