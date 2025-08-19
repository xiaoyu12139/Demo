const { ipcRenderer } = require('electron');
const fs = require('fs');
const path = require('path');

// DOM元素引用
const textEditor = document.getElementById('textEditor');
const clearBtn = document.getElementById('clearBtn');
const saveBtn = document.getElementById('saveBtn');
const notificationBtn = document.getElementById('notificationBtn');
const dialogBtn = document.getElementById('dialogBtn');
const fileBtn = document.getElementById('fileBtn');
const statusText = document.getElementById('statusText');
const currentTime = document.getElementById('currentTime');
const themeButtons = document.querySelectorAll('.theme-btn');

// 版本信息元素
const appVersion = document.getElementById('appVersion');
const nodeVersion = document.getElementById('nodeVersion');
const electronVersion = document.getElementById('electronVersion');
const chromeVersion = document.getElementById('chromeVersion');

// 应用初始化
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
    updateTime();
    loadVersionInfo();
    loadTheme();
});

// 初始化应用
function initializeApp() {
    updateStatus('应用已启动');
    
    // 加载保存的文本内容
    const savedText = localStorage.getItem('editorText');
    if (savedText) {
        textEditor.value = savedText;
    }
    
    // 自动保存功能
    textEditor.addEventListener('input', () => {
        localStorage.setItem('editorText', textEditor.value);
        updateStatus('文本已自动保存');
    });
}

// 设置事件监听器
function setupEventListeners() {
    // 清空按钮
    clearBtn.addEventListener('click', () => {
        textEditor.value = '';
        localStorage.removeItem('editorText');
        updateStatus('文本已清空');
    });
    
    // 保存按钮
    saveBtn.addEventListener('click', saveTextToFile);
    
    // 通知按钮
    notificationBtn.addEventListener('click', showNotification);
    
    // 对话框按钮
    dialogBtn.addEventListener('click', showDialog);
    
    // 文件选择按钮
    fileBtn.addEventListener('click', selectFile);
    
    // 主题切换按钮
    themeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const theme = btn.dataset.theme;
            setTheme(theme);
        });
    });
    
    // 键盘快捷键
    document.addEventListener('keydown', handleKeyboardShortcuts);
}

// 加载版本信息
async function loadVersionInfo() {
    try {
        // 获取应用版本
        const version = await ipcRenderer.invoke('get-app-version');
        appVersion.textContent = version;
        
        // 获取Node.js版本
        nodeVersion.textContent = process.versions.node;
        
        // 获取Electron版本
        electronVersion.textContent = process.versions.electron;
        
        // 获取Chrome版本
        chromeVersion.textContent = process.versions.chrome;
    } catch (error) {
        console.error('加载版本信息失败:', error);
        appVersion.textContent = '未知';
    }
}

// 保存文本到文件
async function saveTextToFile() {
    const text = textEditor.value;
    if (!text.trim()) {
        updateStatus('没有内容可保存');
        return;
    }
    
    try {
        const result = await ipcRenderer.invoke('show-message-box', {
            type: 'question',
            buttons: ['保存', '取消'],
            defaultId: 0,
            title: '保存文件',
            message: '确定要保存当前文本内容吗？',
            detail: '文件将保存到桌面'
        });
        
        if (result.response === 0) {
            const fileName = `electron-demo-${new Date().toISOString().slice(0, 10)}.txt`;
            const filePath = path.join(require('os').homedir(), 'Desktop', fileName);
            
            fs.writeFileSync(filePath, text, 'utf8');
            updateStatus(`文件已保存: ${fileName}`);
            
            // 显示成功通知
            new Notification('保存成功', {
                body: `文件已保存到桌面: ${fileName}`,
                icon: path.join(__dirname, 'assets/icon.png')
            });
        }
    } catch (error) {
        console.error('保存文件失败:', error);
        updateStatus('保存文件失败');
    }
}

// 显示通知
function showNotification() {
    if ('Notification' in window) {
        const notification = new Notification('Electron Demo', {
            body: '这是一个来自Electron应用的通知！',
            icon: path.join(__dirname, 'assets/icon.png'),
            tag: 'demo-notification'
        });
        
        notification.onclick = () => {
            updateStatus('通知被点击了');
        };
        
        updateStatus('通知已发送');
    } else {
        updateStatus('浏览器不支持通知');
    }
}

// 显示对话框
async function showDialog() {
    try {
        const result = await ipcRenderer.invoke('show-message-box', {
            type: 'info',
            buttons: ['确定', '取消', '更多信息'],
            defaultId: 0,
            title: 'Electron Demo',
            message: '这是一个演示对话框',
            detail: '你可以选择不同的按钮来测试对话框功能。\n\n当前时间: ' + new Date().toLocaleString()
        });
        
        const responses = ['确定', '取消', '更多信息'];
        updateStatus(`对话框响应: ${responses[result.response]}`);
    } catch (error) {
        console.error('显示对话框失败:', error);
        updateStatus('显示对话框失败');
    }
}

// 选择文件
function selectFile() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.txt,.md,.js,.json';
    
    input.onchange = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                textEditor.value = e.target.result;
                updateStatus(`文件已加载: ${file.name}`);
            };
            reader.readAsText(file);
        }
    };
    
    input.click();
}

// 主题管理
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('selectedTheme', theme);
    
    // 更新按钮状态
    themeButtons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.theme === theme) {
            btn.classList.add('active');
        }
    });
    
    updateStatus(`主题已切换: ${getThemeName(theme)}`);
}

function loadTheme() {
    const savedTheme = localStorage.getItem('selectedTheme') || 'light';
    setTheme(savedTheme);
}

function getThemeName(theme) {
    const names = {
        light: '浅色',
        dark: '深色',
        blue: '蓝色'
    };
    return names[theme] || theme;
}

// 键盘快捷键处理
function handleKeyboardShortcuts(event) {
    if (event.ctrlKey || event.metaKey) {
        switch (event.key) {
            case 's':
                event.preventDefault();
                saveTextToFile();
                break;
            case 'n':
                event.preventDefault();
                textEditor.value = '';
                updateStatus('新建文档');
                break;
            case '1':
                event.preventDefault();
                setTheme('light');
                break;
            case '2':
                event.preventDefault();
                setTheme('dark');
                break;
            case '3':
                event.preventDefault();
                setTheme('blue');
                break;
        }
    }
}

// 更新状态文本
function updateStatus(message) {
    statusText.textContent = message;
    console.log(`[状态] ${message}`);
    
    // 3秒后恢复默认状态
    setTimeout(() => {
        if (statusText.textContent === message) {
            statusText.textContent = '就绪';
        }
    }, 3000);
}

// 更新时间显示
function updateTime() {
    const now = new Date();
    currentTime.textContent = now.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

// 每秒更新时间
setInterval(updateTime, 1000);

// IPC消息监听
ipcRenderer.on('menu-new-file', () => {
    textEditor.value = '';
    localStorage.removeItem('editorText');
    updateStatus('新建文件');
});

ipcRenderer.on('menu-open-file', (event, filePath) => {
    try {
        const content = fs.readFileSync(filePath, 'utf8');
        textEditor.value = content;
        updateStatus(`文件已打开: ${path.basename(filePath)}`);
    } catch (error) {
        console.error('打开文件失败:', error);
        updateStatus('打开文件失败');
    }
});

// 窗口加载完成事件
window.addEventListener('load', () => {
    updateStatus('界面加载完成');
});

// 窗口关闭前保存数据
window.addEventListener('beforeunload', () => {
    localStorage.setItem('editorText', textEditor.value);
});

// 导出功能供调试使用
window.electronDemo = {
    updateStatus,
    setTheme,
    saveTextToFile,
    showNotification,
    showDialog
};

console.log('Electron Demo 渲染进程已初始化');
console.log('可用的调试命令:', Object.keys(window.electronDemo));