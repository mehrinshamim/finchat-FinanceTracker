import { toast as sonnerToast } from "sonner"

const useToast = () => {
  return {
    toast: ({ title, description, variant = "default", ...props }) => {
      sonnerToast[variant === "destructive" ? "error" : "default"]({
        title,
        description,
        ...props,
      })
    }
  }
}

export { useToast }