type EventCallback = (data: any) => void;

export async function connectEventStream(callbacks: {
  onDropReceived?: EventCallback;
  onStageAdvanced?: EventCallback;
}): Promise<() => void> {
  const token = localStorage.getItem("session_token");
  if (!token) return () => {};

  const controller = new AbortController();

  try {
    const response = await fetch("/api/events/stream", {
      headers: { Authorization: `Bearer ${token}` },
      signal: controller.signal,
    });

    if (!response.ok) return () => {};
    if (!response.body) return () => {};

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    async function read() {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          try {
            const { event, data } = JSON.parse(line.slice(6));
            if (event === "drop_received" && callbacks.onDropReceived) {
              callbacks.onDropReceived(data);
            } else if (event === "stage_advanced" && callbacks.onStageAdvanced) {
              callbacks.onStageAdvanced(data);
            }
          } catch {
            // ignore parse errors
          }
        }
      }
    }

    read().catch(() => {});
  } catch {
    // connection error
  }

  return () => controller.abort();
}
