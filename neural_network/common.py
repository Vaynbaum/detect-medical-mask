import cv2
def draw_text(img, text,
          font=cv2.FONT_HERSHEY_PLAIN,
          pos=(0, 0),
          font_scale=3,
          font_thickness=2,
          text_color=(0, 255, 0),
          text_color_bg=(0, 0, 0)
          ):
    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(img, pos, (20+x + text_w, 20+y + text_h), text_color_bg, -1)
    cv2.putText(img, text, (10+x, 10+y + text_h + font_scale - 1), font, font_scale, text_color, font_thickness)