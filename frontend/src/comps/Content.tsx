import React from "react";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";

const Content = ({ content }) => {

  console.log(content)

  return (
    <ScrollArea className="w-1/2 h-full rounded-md border pr-4 ">
      

      {content.map((item, index) => {
        return (
         <div>{item.address}</div>
        )
      })}



    </ScrollArea>
  );
};

export default Content;

