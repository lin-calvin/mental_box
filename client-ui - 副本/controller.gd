extends Node

signal on_ocr_event(str)
signal on_llm_event(str)
signal on_print_finish(str)

var http_event_source: HTTPEventSource

var SERVER_BASE="http://127.0.0.1:8080/";

var STATE=""	
func _ready() -> void:
	http_event_source = HTTPEventSource.new()
	http_event_source.connect_to_url(SERVER_BASE+"event")
	http_event_source.event.connect(func(ev: ServerSentEvent):
		var data=JSON.parse_string(ev.data)
		print(data)
		match data["event"]:
			"ocr":
				emit_signal("on_ocr_event",data['data'])
			"final":
				emit_signal("on_llm_event",data['data'])
			"print_finish":
				emit_signal("on_print_finish")
	)
func _process(_delta: float) -> void:
	http_event_source.poll()

func on_printer_finished():
	$"../Button".visible=true
	$"../StreamedText".visible=false

func start() -> void:
	$"../Button".visible=false
	$"../StreamedText".visible=true
	var http_request = HTTPRequest.new()
	add_child(http_request)
#    http_request.connect("request_completed", self, "_on_request_completed")
	
	# Send simple GET request
	var error = http_request.request(SERVER_BASE + "run")
	if error != OK:
		push_error("HTTP request failed: " + str(error))
