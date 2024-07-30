from ai71 import AI71 

AI71_API_KEY = "api71-api-6dd3d588-9263-42e2-998c-1f21c54ffc0c"
async def llm_call(prompt):
    response_chunks = []
    for chunk in AI71(AI71_API_KEY).chat.completions.create(
        model="tiiuae/falcon-180b-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{prompt}"},
        ],
        stream=True,
    ):
        if chunk.choices[0].delta.content:
            response_chunks.append(chunk.choices[0].delta.content)
            # print(chunk.choices[0].delta.content, sep="", end="", flush=True)
    
    # Combine all chunks to form the complete response
    response = ''.join(response_chunks)
    return response  

async def llm_response(prompt):
    response_chunks = []
    for chunk in AI71(AI71_API_KEY).chat.completions.create(
        model="tiiuae/falcon-180b-chat",
        messages=[
            {"role": "system", "content": "You are an assistant tasked with generating and rephrasing data for humans. should have greeting message .When given a piece of data, provide a rephrased version that is clear, concise, and human-readable.Ensure that the city is extracted from the address and used appropriately. you should not mention it is rephrased content"},
            {"role": "user", "content": f"{prompt}"},
        ],
        stream=True,
    ):
        if chunk.choices[0].delta.content:
            response_chunks.append(chunk.choices[0].delta.content)
            # print(chunk.choices[0].delta.content, sep="", end="", flush=True)
    
    # Combine all chunks to form the complete response
    response = ''.join(response_chunks)
    return response  
       
    
async def llm_call_function_call(  tool: list[dict], messages: list[dict], temperature: float=1, max_tokens: int=2408):
    try:
        for chunk in AI71(AI71_API_KEY).chat.completions.create(
            model="tiiuae/falcon-180b-chat",
            temperature=temperature,
            max_tokens=max_tokens,
            messages=messages,
            tools=tool,
            tool_choice="auto",
         ):
        
            if chunk.choices[0].delta.content:
                response = chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, sep="", end="", flush=True)

        return response

    except Exception as e:
        if hasattr(e, 'status'):
            if e.status == 400:
                return {
                    "response": "Your prompt violates our content policy, please open a new conversation",
                    "implicit_output": None,
                    "response_type": None,
                }
            elif e.status == 500:
                return {
                    "response": "An unexpected error occurred, please try again later",
                    "implicit_output": None,
                    "response_type": None,
                }
        return {"error": f"An unexpected error occurred: {str(e)}"}