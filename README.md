# Mục Lục
1. [Simple Chatbot sử dụng Streamlit](#simple-chatbot-sử-dụng-streamlit)
2. [Ứng dụng Sửa Lỗi Từ bằng Khoảng Cách Levenshtein](#ứng-dụng-sửa-lỗi-từ-bằng-khoảng-cách-levenshtein)
3. [Ứng dụng Object Detection sử dụng Streamlit](#ứng-dụng-object-detection-sử-dụng-streamlit)
4. [Tài liệu tham khảo](#tài-liệu-tham-khảo)

# Simple ChatBot sử dụng Streamlit

Đây là một ứng dụng ChatBot đơn giản được xây dựng bằng Streamlit và sử dụng API của Hugging Face để tạo phản hồi.

## Yêu cầu

Để chạy ứng dụng này, bạn cần cài đặt các thư viện sau:

- Python 3.6 trở lên
- Streamlit
- Hugchat
- Pytest (cho việc kiểm thử)
- Coverage (cho việc đo coverage)

## Cài đặt

1. **Tạo môi trường ảo (tuỳ chọn nhưng được khuyến khích):**

    ```bash
    python -m venv env
    source env/bin/activate  # Trên Unix hoặc MacOS
    .\env\Scripts\activate   # Trên Windows
    ```

2. **Cài đặt các thư viện cần thiết:**

    ```bash
    pip install streamlit hugchat pytest coverage
    ```

## Chạy ứng dụng

1. **Lưu mã nguồn ứng dụng vào một file, ví dụ `streamlit_app/pages/chatbot.py`:**

2. **Chạy ứng dụng bằng Streamlit:**

    ```bash
    streamlit run streamlit_app/pages/chatbot.py
    ```

    Ứng dụng sẽ tự động mở trong trình duyệt web mặc định của bạn tại địa chỉ `http://localhost:8501`.

## Kiểm thử

1. **Tạo file kiểm thử `test_smoke_streamlit_chatbot.py` để kiểm tra hàm `generate_response`:**

    ```python
   from streamlit.testing.v1 import AppTest

    def test_smoke_page():
        at = AppTest.from_file('../../streamlit_app/pages/chatbot.py')
        at.run()
        assert not at.exception

    ```

2. **Chạy các bài kiểm thử:**

    ```bash
    pytest test_generate_response.py
    ```
   
    ```bash
    coverage run -m pytest -p no:warnings tests/streamlit_chatbot/test_smoke_streamlit_chatbot.py
    ```

## Sử dụng GitHub Actions để tự động kiểm thử

1. **Tạo thư mục `.github/workflows` trong dự án của bạn.**

2. **Tạo file `app_testing.yml` trong thư mục `.github/workflows` với nội dung sau:**

   ```yaml
   name: App testing

   on:
      push:
         branches: [ "main" ]
      pull_request:
         types: [opened, synchronize, reopened]

   permissions:
      contents: read

   jobs:
      streamlit:
         runs-on: ubuntu-latest
         steps:
            - uses: actions/checkout@v4
            - uses: actions/setup-python@v5
              with:
               python-version: '3.11'
            - uses: streamlit/streamlit-app-action@v0.0.3
              with:
               app-path: streamlit_app/streamlit_app.py
               ruff: true
               pytest-args: -v --junit-xml=test-results.xml
            - if: always()
              uses: pmeier/pytest-results-action@v0.6.0
              with:
               path: test-results.xml
               summary: true
               display-options: fEX
    ```

3. **Đẩy mã nguồn và cấu hình lên GitHub:**

    ```bash
    git add .
    git commit -m "Add GitHub Actions workflow for testing"
    git push origin main
    ```

Sau khi đẩy mã nguồn lên, GitHub Actions sẽ tự động chạy các kiểm thử mỗi khi có thay đổi mã nguồn hoặc có yêu cầu kéo (pull request).

## Sử dụng GitHub Actions để tự động kiểm thử và upload coverage lên SonarCloud

1. **Tạo tài khoản và cấu hình SonarCloud:**

    - Đăng ký tài khoản trên [SonarCloud](https://sonarcloud.io/).
    - Tạo một dự án mới và lấy `SONAR_TOKEN` từ phần cài đặt dự án.
   
2. **Tạo thư mục `.github/workflows` trong dự án của bạn.**

3. **Tạo file `build.yml` trong thư mục `.github/workflows` với nội dung sau:**

   ```yaml
   name: Build
   on:
      push:
         branches:
         - main
      pull_request:
       types: [opened, synchronize, reopened]
   jobs:
     sonarcloud:
       name: SonarCloud
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
           with:
             fetch-depth: 0  # Shallow clones should be disabled for a better relevancy of analysis
         - name: Setup Python
           uses: actions/setup-python@v2
           with:
             python-version: ${{ matrix.python }}
         - name: Install tox and any other packages
           run: pip install tox
         - name: Run tox
           run: tox -e py
         - name: Upload coverage report (optional)
           uses: actions/upload-artifact@v4
           with:
             name: coverage-report
             path: coverage.xml  # Adjust path based on your report type
         - name: SonarCloud Scan
           uses: SonarSource/sonarcloud-github-action@master
           env:
             GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}  # Needed to get PR information, if any
             SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
    ```

# Ứng dụng Sửa Lỗi Từ bằng Khoảng Cách Levenshtein

Đây là một ứng dụng đơn giản sử dụng Streamlit để sửa lỗi từ dựa trên khoảng cách Levenshtein. Ứng dụng này sẽ so sánh từ nhập vào với một danh sách từ vựng và đưa ra từ đúng gần nhất dựa trên khoảng cách Levenshtein.

Cách chạy chương trình trong Streamlit tương tự như ứng dụng Chatbot.

## Sử dụng ứng dụng

1. Nhập từ bạn muốn kiểm tra vào ô `Word`.
2. Nhấn nút `Compute`.
3. Ứng dụng sẽ tính khoảng cách Levenshtein giữa từ nhập vào và các từ trong danh sách từ vựng, sau đó đưa ra từ đúng gần nhất.

# Ứng dụng Object Detection sử dụng Streamlit

Đây là một ứng dụng đơn giản sử dụng Streamlit để thực hiện object detection trên ảnh. Ứng dụng sử dụng mô hình MobileNet SSD để phát hiện các đối tượng trong ảnh được tải lên.

## Yêu cầu

Để chạy ứng dụng này, bạn cần cài đặt các thư viện sau:

- Python 3.6 trở lên
- Streamlit
- OpenCV
- NumPy
- Pillow

## Cài đặt

1. **Tạo môi trường ảo (tuỳ chọn nhưng được khuyến khích):**

    ```bash
    python -m venv env
    source env/bin/activate  # Trên Unix hoặc MacOS
    .\env\Scripts\activate   # Trên Windows
    ```
   
2. **Cài đặt các thư viện cần thiết:**

    ```bash
    pip install streamlit opencv-python-headless numpy pillow
    ```

3. **Chuẩn bị mô hình MobileNet SSD:**

    Tạo thư mục `model` trong cùng cấp với thư mục chứa file `app.py`, sau đó tải xuống và đặt các file mô hình và cấu hình vào thư mục này:
    - `MobileNetSSD_deploy.caffemodel`
    - `MobileNetSSD_deploy.prototxt.txt`

Cách chạy chương trình trong Streamlit tương tự như ứng dụng Chatbot.

## Sử dụng ứng dụng

1. Truy cập vào địa chỉ `http://localhost:8501` để mở ứng dụng.
2. Nhấn vào nút "Upload Image" để tải lên một ảnh có định dạng `jpg`, `png`, hoặc `jpeg`.
3. Ứng dụng sẽ hiển thị ảnh đã tải lên và thực hiện phát hiện các đối tượng trong ảnh.
4. Ảnh đã được xử lý với các bounding box sẽ được hiển thị bên dưới.
# Tài liệu tham khảo

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Hugging Face](https://huggingface.co/)
- [Pytest Documentation](https://docs.pytest.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [SonarCloud Documentation](https://sonarcloud.io/documentation)