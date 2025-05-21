pyinstaller \
  --onefile \
  --windowed \
  --name "MyApp" \
  --icon "img/logo.png" \
  --add-data "img/logo.png;data" \
  --add-data "fonts/MeriendaOne-Regular.ttf;data" \
  --add-data "utils/delete_api.py;utils" \
  --add-data "utils/drop_image_widget.py;utils" \
  --add-data "utils/message_box.py;utils" \
  --add-data "utils/my_enum.py;utils" \
  --add-data "utils/show_img_widget.py;utils" \
  --add-data "utils/sidebar.py;utils" \
  --add-data "utils/stack_page.py;utils" \
  --add-data "utils/switch_button.py;utils" \
  --add-data "utils/upload_api.py;utils" \
  gitpic.py
