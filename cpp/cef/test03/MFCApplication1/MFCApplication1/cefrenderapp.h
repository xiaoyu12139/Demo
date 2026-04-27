#pragma once
#include "pch.h"
#include "include/cef_app.h"
#include "include/cef_v8.h"
#include "include/cef_process_message.h"

class CEFRenderApp;

class CEFRenderAppExtensionHandler : public CefV8Handler {
public:
	CEFRenderAppExtensionHandler() = default;
	bool Execute(const CefString& name,
		CefRefPtr<CefV8Value> object,
		const CefV8ValueList& arguments,
		CefRefPtr<CefV8Value>& retval,
		CefString& exception) override;
	IMPLEMENT_REFCOUNTING(CEFRenderAppExtensionHandler);
};

class CEFRenderApp : public CefApp, public CefRenderProcessHandler {
public:
	CEFRenderApp() = default;

	CefRefPtr<CefRenderProcessHandler> GetRenderProcessHandler() override { return this; }
	void OnWebKitInitialized() override;

	IMPLEMENT_REFCOUNTING(CEFRenderApp);
};
