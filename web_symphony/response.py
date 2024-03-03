import orjson
from colored import Fore, Style
import typing as t
from .utils import print_red


class OutgoingResponse:
    def __init__(
        self,
        data: dict,
        serialization: t.Union[
            t.Literal["MANUAL"], t.Literal["AUTO"], t.Literal["JSON"]
        ] = "AUTO",
        serialize_func: t.Optional[t.Callable] = None,
        **kwargs,
    ) -> None:
        self.data = data
        self.status = kwargs.get("status", 200)
        self.headers = kwargs.get(
            "headers", {"Content-Type": "application/json", "Connection": "close"}
        )
        self.headers["server"] = "WebSymphony/0.1"
        self._serialization = serialization
        self._serialize_func = serialize_func

    @property
    @print_red
    def body(self) -> bytes:
        try:
            if self._serialization == "AUTO":
                # Preprocess the data to ensure it is fully serializable by orjson.
                # This involves converting bytes to a serializable format within `self.data`.
                def preprocess_data(data):
                    if isinstance(data, bytes):
                        return data.decode("utf-8")  # Convert bytes to string
                    elif isinstance(data, dict):
                        return {k: preprocess_data(v) for k, v in data.items()}
                    elif isinstance(data, list):
                        return [preprocess_data(element) for element in data]
                    else:
                        return data

                # Preprocess `self.data` to ensure all bytes are converted to strings.
                serializable_data = preprocess_data(self.data)

                # Now, serialize the preprocessed data.
                return orjson.dumps(serializable_data)

            elif self._serialization == "MANUAL":
                if self._serialize_func:
                    serialized_data = self._serialize_func(self.data)
                    if isinstance(serialized_data, bytes):
                        return serialized_data
                    else:
                        return str(serialized_data).encode()
                else:
                    raise ValueError(
                        f"{Fore.RED}Serialization function not provided for manual serialization{Style.RESET}"
                    )

            elif self._serialization == "JSON":
                return orjson.dumps(self.data)

        except Exception as e:
            raise TypeError(
                f"{Fore.RED}{e}{Style.RESET} {Fore.BLUE}Please ensure the data can be serialized or provide a custom serialization function.{Style.RESET}"
            )

    def __bytes__(self) -> bytes:
        return self.build_response()

    def build_response(self) -> bytes:
        response_line = (
            f"HTTP/1.1 {self.status} {'OK' if self.status == 200 else 'Not Found'}\r\n"
        )
        headers = "".join(f"{key}: {value}\r\n" for key, value in self.headers.items())
        headers += f"Content-Length: {len(self.body)}\r\n\r\n"
        return response_line.encode() + headers.encode() + self.body
