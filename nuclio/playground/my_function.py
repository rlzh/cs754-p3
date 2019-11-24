import os


# command to run this using config file 'function.yaml' (metadata.namespace in config file seems to be broken?!?)
"""
 nuctl deploy my-function -p ./nuclio/my_function.py \
	 	--namespace nuclio \
 		--file ./nuclio/function.yaml \
 		--registry $(minikube ip):5000 --run-registry localhost:5000 
"""


def my_entry_point(context, event):

	# use the logger, outputting the event body
	context.logger.info_with('Got invoked',
		trigger_kind=event.trigger.kind,
		event_body=event.body,
		some_env=os.environ.get('MY_ENV_VALUE'))
	# return a response
	context.user_data.my_var += 1 
	# return str(context.user_data.my_var)
	return str(fib(40))


def init_context(context):

    # Create the DB connection under "context.user_data"
    setattr(context.user_data, 'my_var', 0)


def fib(n):
	if n == 0:
		return 0
	elif n == 1:
		return 1
	
	return fib(n-1) + fib(n-2)



    