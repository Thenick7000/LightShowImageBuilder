import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPainter, QPixmap, QPen, QColor
from PyQt6.QtCore import Qt, QPoint


class DrawingCanvas(QWidget):

    def __init__ (self):
        super().__init__()
        self.setMinimumSize(400,300)
        self.canvas_image = None
        self.last_point = QPoint()
        self.pen_color = QColor(Qt.GlobalColor.black)
        self.pen_width = 4

    def resizeEvent(self, event):

        super().resizeEvent(event)
        new_canvas = QPixmap(self.size())
        new_canvas.fill(Qt.GlobalColor.white)
        if self.canvas_image is not None:
            painter = QPainter(new_canvas)
            painter.drawPixmap(0,0,self.canvas_image)
            painter.end
        self.canvas_image = new_canvas

    def paintEvent(self, event):

        painter = QPainter(self)
        if self.canvas_image is not None:
            painter.drawPixmap(0,0,self.canvas_image)
        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_point = event.position().toPoint()
            

    def mouseMoveEvent(self,event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            current_point = event.position().toPoint()
            painter = QPainter(self.canvas_image)

            pen = QPen(
                self.pen_color,
                self.pen_width,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
                Qt.PenJoinStyle.RoundJoin)

            painter.setPen(pen)

            painter.drawLine(self.last_point, current_point)
            painter.end()

            self.last_point = current_point

            self.update()

    def clear_canvas(self):
        if self.canvas_image is not None:
            self.canvas_image.fill(Qt.GlobalColor.white)
            self.update()


class DfCanvas(QMainWindow):
    
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blank Canvas")
        self.resize(700, 500)
    

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.main_layout = QVBoxLayout()
        central_widget.setLayout(self.main_layout)

        self.canvas = DrawingCanvas()
        self.main_layout.addWidget(self.canvas)

        clear_button = QPushButton("Clear")

        clear_button.clicked.connect(self.canvas.clear_canvas)

        self.main_layout.addWidget(clear_button)
      

def main():
    app = QApplication(sys.argv)
        
    window = DfCanvas()
    window.show()
    
    sys.exit(app.exec())
   

# Execution block
if __name__ == "__main__":
    main()