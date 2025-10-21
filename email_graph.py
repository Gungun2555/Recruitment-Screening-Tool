
class FakeStateGraph:
    def add_node(self, name, func): 
        self.func = func
    def add_edge(self, a, b): 
        pass
    def compile(self): 
        return self
    def invoke(self, state):
        skill_match = state["skill_match"]
        experience = state["experience_level"]
        now = state["now"]

        if skill_match == "Match":
            return {
                "subject": "🎉 Congratulations! You’re Selected at LangGraph!",
                "body": f"""
Dear Candidate,

We are thrilled to inform you that after a thorough evaluation of your skills, qualifications, and experience, you have been selected for the role at LangGraph! 🌟
Your impressive technical expertise, problem-solving abilities, and enthusiasm for innovation truly stood out among the applicants.
Our HR team will reach out shortly with onboarding details, documentation requirements, and a schedule for your first Google Meet session with the team.
📅 Date: {now}
💻 Google Meet link: https://meet.google.com/unh-mbep-njk

Warm regards,  
Gungun Sachdeva  
Co-founder, LangGraph Company"""
            }
        elif "Senior" in experience:
            return {
                "subject": "Application Status — LangGraph",
                "body": """
Dear Candidate,

Thank you for your application and the time you took to interview with us. While we found your experience impressive, your profile does not align with the current role requirements. 🙏
We truly appreciate your expertise and invite you to apply again for senior openings in the future.
For any queries, feel free to reach out at 8700021988.

Location: Sector 15, Palava City, Dombivli (Mumbai)
Wishing you the very best in your career journey.
Warm regards, 
Gungun Sachdeva 
Co-founder, LangGraph Company"""
            }
        else:
            return {
                "subject": "Job Application Update",
                "body": "Dear Candidate,\n\nUnfortunately, your profile does not match.\n"
            }

# Expose the dummy classes as StateGraph and END
StateGraph = FakeStateGraph
END = "end"
