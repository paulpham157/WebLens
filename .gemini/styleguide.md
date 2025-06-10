# Style Guide cho Dự Án WebLens

# Important
When chatting with the user, use Vietnamese language to explain to the user.

# Introduction
Tài liệu này đưa ra các quy tắc lập trình và quy ước code cho dự án WebLens. WebLens là một framework testing hiện đại được phát triển để thay thế các framework BDD truyền thống, sử dụng browser-use cloud API để tự động hóa trình duyệt.

# Key Principles
* **Readability:** Code phải dễ đọc và dễ hiểu cho tất cả thành viên trong team.
* **Maintainability:** Code phải dễ sửa đổi và mở rộng khi cần thiết.
* **Consistency:** Tuân thủ style thống nhất giúp nâng cao hiệu quả làm việc nhóm và giảm lỗi.
* **Performance:** Hiệu suất cũng quan trọng, đặc biệt là với framework testing.
* **Cloud-First:** Thiết kế luôn hướng đến việc sử dụng cloud API thay vì local browsers.

# Coding Conventions

## Indentation và Formatting
* **Sử dụng 4 khoảng trắng cho mỗi cấp indent.**
* **Tối đa 120 ký tự trên một dòng.**
* **Blank lines:** Sử dụng 2 dòng trống giữa các class, 1 dòng trống giữa các method.

## Quy Tắc Python
* **Docstrings:** Tất cả module, class và function phải có docstring theo chuẩn Google Python Style.
* **Type Hints:** Luôn sử dụng type hints cho parameters và return types.
* **Imports:** Sắp xếp theo thứ tự: standard library, third-party packages, local imports.
* **Async/Await:** Sử dụng async/await nhất quán, không trộn lẫn với các phương pháp non-async.

## Kiến Trúc WebLens
* **Browser Management:** Luôn sử dụng browser-use cloud API, không sử dụng Playwright trực tiếp.
* **Configuration:** Sử dụng `.env` cho cấu hình, không hardcode API keys hoặc thông tin nhạy cảm.
* **Tests:** Sử dụng TestRunner API mới (không còn tham số browsers và profiles).
* **Error Handling:** Đảm bảo xử lý lỗi chi tiết và có cơ chế fallback.

## Logging
* **Log Levels:** Sử dụng đúng log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
* **Context:** Logs phải có đủ context để debug khi cần thiết.
* **Cấu trúc:** Format log thống nhất: thời gian, mức độ, module, message.

## Testing
* **Test Coverage:** Mỗi thành phần core phải có unit tests, integration tests.
* **Mocking:** Sử dụng mock objects cho browser-use cloud API trong tests.
* **Naming:** Tên test phải mô tả rõ hành vi đang test, format: test_{function}_{scenario}_{expected_result}.

## Documentation

* **README:** Cập nhật README khi có thay đổi API hoặc cách sử dụng.
* **Examples:** Mỗi tính năng mới phải có ví dụ trong thư mục examples/.
* **CHANGELOG:** Cập nhật CHANGELOG cho mỗi phiên bản mới.

## Git Workflow

* **Commit Messages:** Prefix với loại thay đổi: feat:, fix:, docs:, test:, refactor:
* **Branch Naming:** feature/{feature-name}, bugfix/{issue-number}
* **Pull Requests:** Mô tả đầy đủ thay đổi, đính kèm screenshots nếu liên quan đến UI
* **Code Reviews:** Mỗi PR phải được review bởi ít nhất 1 team member khác
* **CI/CD:** Tất cả tests phải pass trên CI trước khi merge

## Standard Libraries và Dependencies

* **Browser-use:** Sử dụng browser-use cloud API làm cốt lõi cho automation
* **Python-dotenv:** Quản lý biến môi trường và API keys
* **Conda:** Sử dụng Conda để quản lý môi trường phát triển
* **pytest:** Framework testing chính cho dự án

## Quy Định Đặc Biệt

* **Không sử dụng Playwright trực tiếp:** Mọi tương tác với browser phải thông qua browser-use cloud API
* **Luôn fallback gracefully:** Cung cấp mock functionality khi không có API key
* **Luôn check version** khi tung ra bản mới
* **Nhất quán API:** Không sử dụng tham số browsers và profiles cho hàm run_tests()
* **Bảo mật API keys:** Không bao giờ commit API keys thật vào repository
