#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QLabel>
#include <QtWidgets/QSlider>
#include <QtWidgets/QVBoxLayout>
#include <QtCore/QDebug>

class MainWindow : public QMainWindow {
    Q_OBJECT
public:
    MainWindow() {
        auto *central = new QWidget(this);
        auto *layout = new QVBoxLayout(central);

        label = new QLabel("Ready", central);
        auto *btn = new QPushButton("Emit textEmitted", central);
        auto *slider = new QSlider(Qt::Horizontal, central);
        slider->setRange(0, 100);

        layout->addWidget(label);
        layout->addWidget(btn);
        layout->addWidget(slider);
        setCentralWidget(central);
        setWindowTitle("Demo GUI - Signals/Slots");

        connect(btn, &QPushButton::clicked, this, [this]() {
            emit textEmitted("Button clicked!");
        });
        connect(slider, &QSlider::valueChanged, this, &MainWindow::setValue);
        connect(this, &MainWindow::textEmitted, this, &MainWindow::onTextReceived);
        connect(this, &MainWindow::valueChanged, this, &MainWindow::onValueChanged);

        const quint64 addr = reinterpret_cast<quint64>(this);
        qInfo() << "[demo_gui] MainWindow address:" << QString("0x%1").arg(addr, 0, 16);
        label->setText(QString("MainWindow addr: 0x%1").arg(addr, 0, 16));
    }

signals:
    void valueChanged(int value);
    void textEmitted(const QString &text);

public slots:
    void setValue(int v) { emit valueChanged(v); }
    void onTextReceived(const QString &t) { label->setText(t); }
    void onValueChanged(int v) { label->setText(QString("Value: %1").arg(v)); }

private:
    QLabel *label {nullptr};
};

int main(int argc, char **argv) {
    QApplication app(argc, argv);
    MainWindow w;
    w.resize(400, 200);
    w.show();
    return app.exec();
}

#include "main.moc"