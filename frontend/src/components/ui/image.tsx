
import * as React from "react"
import { cn } from "@/lib/utils"

export interface ImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
  aspectRatio?: "square" | "video" | "wide" | "auto"
  className?: string
}

const Image = React.forwardRef<HTMLImageElement, ImageProps>(
  ({ aspectRatio = "auto", className, alt = "", ...props }, ref) => {
    const aspectRatioClass = {
      square: "aspect-square",
      video: "aspect-video",
      wide: "aspect-[21/9]",
      auto: "aspect-auto"
    }[aspectRatio]

    return (
      <img
        ref={ref}
        className={cn(
          "rounded-md object-cover",
          aspectRatioClass,
          className
        )}
        alt={alt}
        {...props}
      />
    )
  }
)
Image.displayName = "Image"

export default Image
