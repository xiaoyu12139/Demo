#pragma once
#include "pch.h"
#include "include/cef_client.h"
#include "include/cef_process_message.h"

enum { WM_CEF_JS_CALL = WM_APP + 200 };

class CEFBrowserClient : public CefClient {
public:
	explicit CEFBrowserClient(HWND host) : m_host(host) {}

	bool OnProcessMessageReceived(CefRefPtr<CefBrowser> browser,
		CefRefPtr<CefFrame> frame,
		CefProcessId source_process,
		CefRefPtr<CefProcessMessage> message) override;

	IMPLEMENT_REFCOUNTING(CEFBrowserClient);

private:
	HWND m_host = nullptr;
};

class CEFDialog : public CDialogEx
{
	// Construction
public:
	CEFDialog(CWnd* pParent = nullptr);	

	CefRefPtr<CEFBrowserClient> m_CEFClient;

protected:
	virtual BOOL OnInitDialog();
	afx_msg LRESULT OnCefJsCall(WPARAM wParam, LPARAM lParam);
	DECLARE_MESSAGE_MAP()
};
