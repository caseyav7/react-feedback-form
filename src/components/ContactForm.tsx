import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Card } from "@/components/ui/card";
import { CheckCircle2 } from "lucide-react";

const formSchema = z.object({
  title: z.string().trim().min(1, { message: "Title is required" }).max(100, { message: "Title must be less than 100 characters" }),
  firstName: z.string().trim().min(1, { message: "First name is required" }).max(100, { message: "First name must be less than 100 characters" }),
  email: z.string().trim().email({ message: "Please enter a valid email address" }).max(255, { message: "Email must be less than 255 characters" }),
  age: z.string().min(1, { message: "Age is required" }),
  feedback: z.string().trim().min(1, { message: "Feedback is required" }).max(1000, { message: "Feedback must be less than 1000 characters" }),
});

type FormData = z.infer<typeof formSchema>;

const ContactForm = () => {
  const [isSubmitted, setIsSubmitted] = useState(false);

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      title: "",
      firstName: "",
      email: "",
      age: "",
      feedback: "",
    },
  });

  const onSubmit = (data: FormData) => {
    console.log("Form submitted:", data);
    setIsSubmitted(true);
    form.reset();
    
    // Hide success message after 5 seconds
    setTimeout(() => {
      setIsSubmitted(false);
    }, 5000);
  };

  // Generate age options 1-100
  const ageOptions = Array.from({ length: 100 }, (_, i) => i + 1);

  if (isSubmitted) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-background via-background to-accent/5 px-4">
        <Card className="w-full max-w-md p-8 text-center space-y-4 animate-in fade-in zoom-in duration-500">
          <div className="flex justify-center">
            <CheckCircle2 className="w-16 h-16 text-primary" />
          </div>
          <h2 className="text-2xl font-bold text-foreground">Thank You!</h2>
          <p className="text-muted-foreground">
            Thank you for your feedback! Your message has been submitted successfully.
          </p>
        </Card>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-background via-background to-accent/5 px-4 py-8">
      <Card className="w-full max-w-md p-8 space-y-6 shadow-xl animate-in fade-in slide-in-from-bottom-4 duration-700">
        <div className="space-y-2 text-center">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            Contact Us
          </h1>
          <p className="text-muted-foreground">
            We'd love to hear from you. Please fill out this form.
          </p>
        </div>

        <Form {...form}>
          <form id="contactForm" noValidate onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="title"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Title</FormLabel>
                  <FormControl>
                    <Input 
                      placeholder="e.g., Mr., Ms., Dr." 
                      {...field}
                      className="transition-all focus:ring-2 focus:ring-primary/20"
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="firstName"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>First Name</FormLabel>
                  <FormControl>
                    <Input 
                      placeholder="Enter your first name" 
                      {...field}
                      className="transition-all focus:ring-2 focus:ring-primary/20"
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input 
                      type="email"
                      placeholder="your.email@example.com" 
                      {...field}
                      className="transition-all focus:ring-2 focus:ring-primary/20"
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="age"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Age</FormLabel>
                  <Select onValueChange={field.onChange} value={field.value}>
                    <FormControl>
                      <SelectTrigger className="transition-all focus:ring-2 focus:ring-primary/20">
                        <SelectValue placeholder="Select your age" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent className="max-h-[200px]">
                      {ageOptions.map((age) => (
                        <SelectItem key={age} value={age.toString()}>
                          {age}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="feedback"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Feedback</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Share your thoughts with us..."
                      className="min-h-[120px] resize-none transition-all focus:ring-2 focus:ring-primary/20"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button 
              type="submit" 
              className="w-full bg-gradient-to-r from-primary to-accent hover:opacity-90 transition-all duration-300 shadow-lg hover:shadow-xl"
            >
              Submit Feedback
            </Button>
          </form>
        </Form>
      </Card>
    </div>
  );
};

export default ContactForm;
