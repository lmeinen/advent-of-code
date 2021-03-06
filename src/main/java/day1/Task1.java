package day1;

import java.io.IOException;
import util.AOCTemplate;

public class Task1 extends AOCTemplate {

    public Task1(String filename) throws IOException {
        super(filename);
    }

    public static void main(String[] args) {
        final Task1 task;
        try {
            task = new Task1("day1.txt");
            task.solve();
        } catch (IOException e) {
            writer.println("Instantiation of task solver failed, aborting...");
        }
        writer.flush();
        writer.close();
    }

    @Override
    public void solve() {
        Integer prevVal = null;
        var numIncreases = 0;
        while (true) {
            try {
                var x = reader.nextInt();
                if (prevVal != null && x > prevVal) {
                    numIncreases++;
                }
                prevVal = x;
            } catch (NullPointerException e) {
                break;
            }
        }
        writer.println("Number of increases: " + numIncreases);
    }
}
