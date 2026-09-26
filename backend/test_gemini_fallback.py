from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch

from gemini_fallback import (
    FREE_TIER_MODEL_ORDER,
    GeminiUnavailableError,
    model_order,
    run_with_gemini_fallback,
)


class GeminiFallbackTests(IsolatedAsyncioTestCase):
    def test_default_model_order_matches_wearthis_ranking(self):
        expected = (
            "gemini-3.5-flash-lite",
            "gemini-3.8-flash",
            "gemini-3.1-flash-lite",
            "gemini-3.7-flash",
            "gemini-3.6-flash",
            "gemini-3.5-flash",
            "gemini-3-flash-preview",
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
        )

        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual(FREE_TIER_MODEL_ORDER, expected)
            self.assertEqual(model_order(), expected)

    async def test_retries_busy_model_three_times_before_fallback(self):
        call = AsyncMock(side_effect=[
            RuntimeError("503 Service Unavailable"),
            RuntimeError("model is experiencing high demand"),
            RuntimeError("503 Service Unavailable"),
            "fallback result",
        ])

        with patch("gemini_fallback.model_order", return_value=("first", "second")), patch(
            "gemini_fallback.asyncio.sleep", new=AsyncMock()
        ):
            result = await run_with_gemini_fallback(call)

        self.assertEqual(result, "fallback result")
        self.assertEqual(call.await_args_list[0].args, ("first",))
        self.assertEqual(call.await_args_list[2].args, ("first",))
        self.assertEqual(call.await_args_list[3].args, ("second",))

    async def test_exhaustion_advances_to_the_next_model_without_retry(self):
        call = AsyncMock(side_effect=[RuntimeError("429 RESOURCE_EXHAUSTED quota"), "fallback result"])

        with patch("gemini_fallback.model_order", return_value=("first", "second")):
            result = await run_with_gemini_fallback(call)

        self.assertEqual(result, "fallback result")
        self.assertEqual([args.args[0] for args in call.await_args_list], ["first", "second"])

    async def test_reports_when_every_model_is_unavailable(self):
        call = AsyncMock(side_effect=RuntimeError("429 RESOURCE_EXHAUSTED quota"))

        with patch("gemini_fallback.model_order", return_value=("only-model",)):
            with self.assertRaises(GeminiUnavailableError):
                await run_with_gemini_fallback(call)
