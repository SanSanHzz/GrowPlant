import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import PlantCanvas from "@/components/plant/PlantCanvas.vue";

describe("PlantCanvas", () => {
  it("renders the plant SVG", () => {
    const wrapper = mount(PlantCanvas, {
      props: { stage: 1, maxStage: false },
    });
    expect(wrapper.find("svg").exists()).toBe(true);
  });

  it("shows max level badge when maxStage is true", () => {
    const wrapper = mount(PlantCanvas, {
      props: { stage: 5, maxStage: true },
    });
    expect(wrapper.text()).toContain("MAX LEVEL");
  });

  it("does not show badge when not max stage", () => {
    const wrapper = mount(PlantCanvas, {
      props: { stage: 1, maxStage: false },
    });
    expect(wrapper.text()).not.toContain("MAX LEVEL");
  });
});
