import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import DropCounter from "@/components/dashboard/DropCounter.vue";

describe("DropCounter", () => {
  it("displays the total drops", () => {
    const wrapper = mount(DropCounter, {
      props: { total: 42 },
    });
    expect(wrapper.text()).toContain("42");
    expect(wrapper.text()).toContain("total drops");
  });

  it("displays zero correctly", () => {
    const wrapper = mount(DropCounter, {
      props: { total: 0 },
    });
    expect(wrapper.text()).toContain("0");
  });
});
