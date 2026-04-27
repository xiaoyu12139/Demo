#include "pch.h"
#include "cefrenderapp.h"

#include <string>

bool CEFRenderAppExtensionHandler::Execute(const CefString& name,
	CefRefPtr<CefV8Value> object,
	const CefV8ValueList& arguments,
	CefRefPtr<CefV8Value>& retval,
	CefString& exception) {
	CefRefPtr<CefV8Context> context = CefV8Context::GetCurrentContext();
	if (!context) {
		exception = "No V8 context";
		return true;
	}

	if (name == "testJS2CPP") {
		//CefRefPtr<CefFrame> frame = context->GetFrame();
		//if (!frame) {
		//	exception = "No frame";
		//	return true;
		//}

		//CefString msg;
		//if (arguments.size() >= 1 && arguments[0]->IsString()) {
		//	msg = arguments[0]->GetStringValue();
		//}

		//CefRefPtr<CefProcessMessage> message = CefProcessMessage::Create("V8Call");
		//CefRefPtr<CefListValue> list = message->GetArgumentList();
		//list->SetString(0, "testJS2CPP");
		//list->SetString(1, msg);
		//frame->SendProcessMessage(PID_BROWSER, message);

		//retval = CefV8Value::CreateBool(true);
		//return true;
		std::string s = "hello";
		AfxMessageBox(CA2W(s.c_str(), CP_UTF8));
	}

	return false;
}

void CEFRenderApp::OnWebKitInitialized() {
	const std::string app_code =
		"var connector;"
		"if (!connector) connector = {};"
		"(function(){"
		"connector.testJS2CPP = function(msg){"
		" native function testJS2CPP();"
		" return testJS2CPP(msg);"
		"};"
		"})();";

	CefRegisterExtension("v8/connector", app_code, new CEFRenderAppExtensionHandler());
}
