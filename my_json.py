import json
import html


def loop_htmlspecialchars(value):
    if isinstance(value, str):
        return html.escape(value)
    elif isinstance(value, list):
        return [loop_htmlspecialchars(v) for v in value]
    elif isinstance(value, dict):
        return {k: loop_htmlspecialchars(v) for k, v in value.items()}
    return value


input_json = (
    '{\"status\":1,\"message\":\"修改云药方运费成功\",\"success\":true,\"data\":{\"deliveryMoney\":24,\"isCanDelivery\":1}}')
data = json.loads(input_json)
data = loop_htmlspecialchars(data)
output_str = json.dumps(data, indent=4, ensure_ascii=False)
print(output_str)
