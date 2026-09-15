package com.example.wearthis.data.local

import android.content.Context
import android.net.Uri
import java.io.File
import java.util.UUID

class ClothingImageStorage(private val context: Context) {
    fun copyIntoAppStorage(sourceUri: Uri): String {
        val directory = File(context.filesDir, CLOTHING_DIRECTORY).apply { mkdirs() }
        val extension = when (context.contentResolver.getType(sourceUri)) {
            "image/png" -> "png"
            "image/webp" -> "webp"
            else -> "jpg"
        }
        val destination = File(directory, "${UUID.randomUUID()}.$extension")

        try {
            val input = requireNotNull(context.contentResolver.openInputStream(sourceUri)) {
                "Unable to read the selected image."
            }
            input.use { source ->
                destination.outputStream().use { target ->
                    source.copyTo(target)
                }
            }
        } catch (error: Throwable) {
            destination.delete()
            throw error
        }

        return destination.absolutePath
    }

    fun delete(localImagePath: String) {
        File(localImagePath).delete()
    }

    private companion object {
        const val CLOTHING_DIRECTORY = "clothing"
    }
}
