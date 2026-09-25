from lambda_api_decorators import get, post

@get('/one')
@post('/two')
def handler(event, context):
    return event['requestContext']['authorizer']['claims']['sub']
