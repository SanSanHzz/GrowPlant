type EventCallback = (data: any) => void;

export async function connectEventStream(callbacks: {
  onDropReceived?: EventCallback;
  onStageAdvanced?: EventCallback;
}): Promise<() => void> {
  let controller = new AbortController();
  let stopped = false;

  async function connect() {
    const token = localStorage.getItem("session_token");
    if (!token) return;

    while (!stopped) {
      try {
        const response = await fetch("/api/events/stream", {
          headers: { Authorization: `Bearer ${token}` },
          signal: controller.signal,
        });

        if (!response.ok || !response.body) {
          await delay(5000);
          continue;
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while (!stopped) {
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
      } catch {
        // connection error, retry
      }

      if (!stopped) await delay(5000);
    }
  }

  connect();

  return () => {
    stopped = true;
    controller.abort();
  };
}

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
