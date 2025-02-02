from app.extensions import client

def send(model='gpt-3.5-turbo', prompt= 'hi'):
    print('a')
    try:
        # Получаем данные из запроса

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            web_search=False
        )

        print(response)

        return ({
            "status": "success",
            "message": response.choices[0].message.content
        }), 200
        

    except Exception as e:
        return ({
            "status": "error",
            "message": str(e)
        }), 500
    
print(send())