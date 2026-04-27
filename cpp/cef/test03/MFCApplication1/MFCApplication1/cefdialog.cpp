#include "pch.h"
#include "Resource.h"
#include "cefdialog.h"

BEGIN_MESSAGE_MAP(CEFDialog, CDialogEx)
	ON_MESSAGE(WM_CEF_JS_CALL, &CEFDialog::OnCefJsCall)
END_MESSAGE_MAP()

CEFDialog::CEFDialog(CWnd* pParent /*=nullptr*/)
	: CDialogEx(IDD_CEFDIALOG_DIALOG, pParent)
{
}

BOOL CEFDialog::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	CefWindowInfo windowInfo;
	CefBrowserSettings browserSettings;

	m_CEFClient = new CEFBrowserClient(m_hWnd);

	CRect rc;
	GetClientRect(&rc);
	windowInfo.SetAsChild(m_hWnd, CefRect(0, 0, rc.Width(), rc.Height()));
	CefBrowserHost::CreateBrowser(windowInfo, m_CEFClient, "https://www.baidu.com/", browserSettings, nullptr, nullptr);

	return TRUE;  
}

LRESULT CEFDialog::OnCefJsCall(WPARAM wParam, LPARAM lParam)
{
	auto* text = reinterpret_cast<CString*>(lParam);
	if (text) {
		AfxMessageBox(*text);
		delete text;
	}
	return 0;
}

bool CEFBrowserClient::OnProcessMessageReceived(CefRefPtr<CefBrowser> browser,
	CefRefPtr<CefFrame> frame,
	CefProcessId source_process,
	CefRefPtr<CefProcessMessage> message)
{
	if (!message) {
		return false;
	}

	if (message->GetName() == "V8Call") {
		auto list = message->GetArgumentList();
		const auto method = list->GetString(0);
		if (method == "testJS2CPP") {
			const auto payload = list->GetString(1);
			auto* text = new CString(payload.ToWString().c_str());
			::PostMessage(m_host, WM_CEF_JS_CALL, 0, reinterpret_cast<LPARAM>(text));
			return true;
		}
	}

	return false;
}
