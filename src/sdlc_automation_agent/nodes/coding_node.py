from src.sdlc_automation_agent.state.sdlc_state import SDLCState, UserStoryList
from src.sdlc_automation_agent.utils.Utility import Utility

class CodingNode:
    """
    Graph Node for the Coding
    
    """
    
    def __init__(self, model):
        self.llm = model
        self.utility = Utility()
    
    ## ---- Code Generation ----- ##
    def generate_code(self, state: SDLCState):
        """
            Generates the code for the given SDLC state as multiple Python files.
        """
        print("----- Generating the code ----")
        
        requirements = state.get('requirements', '')
        user_stories = state.get('user_stories', '')
        code_feedback = state.get('code_review_feedback', '') if 'code_generated' in state else ""
        security_feedback = state.get('security_recommendations', '') if 'security_recommendations' in state else ""
        
        prompt = f"""
        Generate a complete Python project organized as multiple code files. 
        Based on the following SDLC state, generate only the Python code files with their complete implementations. 
        Do NOT include any explanations, requirements text, or design document details in the output—only code files with proper names and code content.

        SDLC State:
        ---------------
        Project Name: {state['project_name']}

        Requirements:
        {self.utility.format_list(requirements)}

        User Stories:
        {self.utility.format_user_stories(user_stories)}

        Functional Design Document:
        {state['design_documents']['functional']}

        Technical Design Document:
        {state['design_documents']['technical']}

        {"Note: Incorporate the following code review feedback: " + code_feedback if code_feedback else ""}
        {"Note: Apply the following security recommendations: " + security_feedback if security_feedback else ""}

        Instructions:
        - Structure the output as multiple code files (for example, "main.py", "module1.py", etc.), each separated clearly.
        - Each file should contain only the code necessary for a modular, fully-functional project based on the input state.
        - Do not output any additional text, explanations, or commentary outside the code files.
        - Ensure the code follows Python best practices, is syntactically correct, and is ready for development.
        """
        response = self.llm.invoke(prompt)
        code_review_comments = self.get_code_review_comments(code=response.content)
        return {
                'code_generated': response.content, 
                'code_review_comments': code_review_comments
            }
    
    ## This code review comments will be used while generating test cases
    def get_code_review_comments(self, code: str):
        """
        Generate code review comments for the provided code
        """
        print("----- Generating code review comments ----")
        
        # Create a prompt for the LLM to review the code
        prompt = f"""
            You are a coding expert. Please review the following code and provide detailed feedback:
            ```
            {code}
            ```
            Focus on:
            1. Code quality and best practices
            2. Potential bugs or edge cases
            3. Performance considerations
            4. Security concerns
            
            End your review with an explicit APPROVED or NEEDS_FEEDBACK status.
        """
        
        # Get the review from the LLM
        response = self.llm.invoke(prompt)
        review_comments = response.content
        return review_comments
    
    def code_review(self, state: SDLCState):
        return state
    
    def fix_code(self, state: SDLCState):
        pass
    
    def code_review_router(self, state: SDLCState):
        """
            Evaluates Code review is required or not.
        """
        return state.get("code_review_status", "approved")  # default to "approved" if not present
    
    ## ---- Security Review ----- ##
    def security_review_recommendations(self, state: SDLCState):
        """
            Performs security review of the code generated
        """
        print("----- Generating security recommendations ----")
          
         # Get the generated code from the state
        code_generated = state.get('code_generated', '')

         # Create a prompt for the LLM to review the code for security concerns
        prompt = f"""
            You are a security expert. Please review the following Python code for potential security vulnerabilities:
            ```
            {code_generated}
            ```
            Focus on:
            1. Identifying potential security risks (e.g., SQL injection, XSS, insecure data handling).
            2. Providing recommendations to mitigate these risks.
            3. Highlighting any best practices that are missing.

            End your review with an explicit APPROVED or NEEDS_FEEDBACK status.
        """

         # Invoke the LLM to perform the security review
        response = self.llm.invoke(prompt)
        state["security_recommendations"] =  response.content
        return state
    
    def security_review(self, state: SDLCState):
        return state
    
    def fix_code_after_security_review(self, state: SDLCState):
        pass
    
    def security_review_router(self, state: SDLCState):
        """
            Security Code review is required or not.
        """
        return state.get("security_review_status", "approved")  # default to "approved" if not present
    
    ## ---- Test Cases ----- ##
    def write_test_cases(self, state: SDLCState):
        """
            Generates the test cases based on the generated code and code review comments
        """
        print("----- Generating Test Cases ----")
    
        # Get the generated code and code review comments from the state
        code_generated = state.get('code_generated', '')
        code_review_comments = state.get('code_review_comments', '')

         # Create a prompt for the LLM to generate test cases
        prompt = f"""
            You are a software testing expert. Based on the following Python code and its review comments, generate comprehensive test cases:
            
            ### Code:
            ```
                {code_generated}
                ```

                ### Code Review Comments:
                {code_review_comments}

                Focus on:
                1. Covering all edge cases and boundary conditions.
                2. Ensuring functional correctness of the code.
                3. Including both positive and negative test cases.
                4. Writing test cases in Python's `unittest` framework format.

                Provide the test cases in Python code format, ready to be executed.
        """

        response = self.llm.invoke(prompt)
        state["test_cases"] = response.content

        return state
    
    def review_test_cases(self, state: SDLCState):
        return state
    
    def revise_test_cases(self, state: SDLCState):
        pass
    
    def review_test_cases_router(self, state: SDLCState):
        """
            Evaluates Test Cases review is required or not.
        """
        return state.get("test_case_review_status", "approved")  # default to "approved" if not present
    
    ## ---- QA Testing ----- ##
    def qa_testing(self, state: SDLCState):
        pass