package com.example.wearthis.data.remote

import com.google.gson.JsonElement
import com.google.gson.JsonParser
import retrofit2.HttpException

class ApiException(message: String, cause: Throwable? = null) :
    Exception(message, cause)

fun Throwable.toApiException(fallbackMessage: String): ApiException {
    val message = if (this is HttpException) {
        val errorJson = response()?.errorBody()?.string()
        errorJson?.let(::extractMessage).orEmpty().ifBlank {
            "Request failed (${code()})."
        }
    } else {
        message
    }

    return ApiException(message?.takeIf(String::isNotBlank) ?: fallbackMessage, this)
}

private fun extractMessage(json: String): String {
    return runCatching {
        val root = JsonParser.parseString(json)
        when {
            root.isJsonObject && root.asJsonObject.has("detail") ->
                root.asJsonObject["detail"].toReadableText()
            root.isJsonObject ->
                root.asJsonObject.entrySet().joinToString("\n") { (field, value) ->
                    "${field.replace('_', ' ').replaceFirstChar(Char::uppercase)}: " +
                        value.toReadableText()
                }
            else -> root.toReadableText()
        }
    }.getOrDefault("")
}

private fun JsonElement.toReadableText(): String {
    return when {
        isJsonArray -> asJsonArray.joinToString(", ") { it.toReadableText() }
        isJsonPrimitive -> asString
        else -> toString()
    }
}
